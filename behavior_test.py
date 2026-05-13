import os
import shutil
import tempfile
import sqlite3
import json
from unittest.mock import MagicMock, patch

# Configure temporary paths
temp_dir = tempfile.mkdtemp()
db_path = os.path.join(temp_dir, "test_world.db")
source_index_dir = os.path.join(temp_dir, "source_index")
history_summary_path = os.path.join(temp_dir, "history_summaries.jsonl")
os.makedirs(source_index_dir, exist_ok=True)

os.environ["AI_RPG_DB"] = db_path
os.environ["AI_RPG_SOURCE_INDEX"] = source_index_dir
os.environ["AI_RPG_HISTORY_SUMMARY"] = history_summary_path

# Mock LLM to avoid real calls
with patch("app.llm.call_llm_structured", return_value={"response": "mocked"}), \
     patch("app.llm.call_llm_text", return_value="mocked response"):
    
    from app import world, db

    def test_behavior():
        results = []

        # 1. generate_setup_randomization sends locked fields
        try:
            # Setup initial state
            db.init_db()
            
            # Mocking the prompt generation or checking the arguments passed to LLM
            with patch("app.world.call_llm_structured") as mock_llm:
                mock_llm.return_value = {"name": "Test Name"}
                # Assume locked fields are passed to generate_setup_randomization
                # We want to check if locked_setup contains what we expect
                requested_field = "name"
                locked_setup = {"theme": "cyberpunk"}
                
                val = world.generate_setup_randomization(requested_field, locked_setup)
                
                # Verify return value
                assert val == "Test Name"
                
                # Verify that locked_setup was passed to the prompt generator/LLM call
                # This depends on internal implementation. Let's inspect the call args
                args, kwargs = mock_llm.call_args
                prompt = args[0]
                assert "cyberpunk" in str(prompt)
                results.append("PASS: generate_setup_randomization handles locked fields and returns requested field.")
        except Exception as e:
            results.append(f"FAIL: generate_setup_randomization: {e}")

        # 2. player gameplay aliases cannot be created before turn > 0
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("INSERT INTO gameState (id, turn) VALUES (1, 0) ON CONFLICT(id) DO UPDATE SET turn=0")
                conn.commit()
            
            try:
                world.create_player_alias("Ghost", "Infiltrator")
                results.append("FAIL: Alias created at turn 0.")
            except Exception as e:
                if "turn > 0" in str(e).lower() or "cannot create alias" in str(e).lower():
                    results.append("PASS: Alias creation blocked at turn 0.")
                else:
                    results.append(f"FAIL: Unexpected error at turn 0 alias creation: {e}")
        except Exception as e:
            results.append(f"FAIL: Alias creation check: {e}")

        # 3. after a turn exists, creating a player alias makes it active
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("UPDATE gameState SET turn = 1 WHERE id = 1")
                conn.commit()
            
            world.create_player_alias("Shadow", "Stealthy expert")
            active_alias = world.get_active_alias()
            if active_alias and active_alias['name'] == "Shadow":
                results.append("PASS: Alias created at turn > 0 is active.")
            else:
                results.append(f"FAIL: Alias not active or incorrect. Got: {active_alias}")
        except Exception as e:
            results.append(f"FAIL: Active alias check: {e}")

        # 4. undetected/undisguised negative karma under alias updates alias reputation AND applies true-identity penalty
        try:
            # Reset reputation
            with sqlite3.connect(db_path) as conn:
                conn.execute("UPDATE aliases SET reputation = 0 WHERE name = 'Shadow'")
                conn.execute("UPDATE gameState SET karma = 0 WHERE id = 1")
                conn.commit()
            
            # "undisguised" means disguise_level or similar is low. 
            # Let's use a function that processes an action with karma implications
            # Assuming a function like process_action(action, alias_id, disguise_fail=True)
            # Since I don't know the exact signature, I'll simulate the impact if I were a test script or call the suspected method.
            # Looking at world.py's likely methods... usually handles karma in world.update_karma
            
            # Scenario: Negative karma while using alias 'Shadow', but recognized as player.
            world.apply_karma_change(amount=-10, alias_name="Shadow", recognized=True)
            
            with sqlite3.connect(db_path) as conn:
                alias_rep = conn.execute("SELECT reputation FROM aliases WHERE name = 'Shadow'").fetchone()[0]
                true_karma = conn.execute("SELECT karma FROM gameState WHERE id = 1").fetchone()[0]
            
            # undisguised negative karma: alias gets hit, true identity gets extra penalty
            if alias_rep < 0 and true_karma < -10: # Assuming it leaks full or extra
                 results.append("PASS: Undisguised negative karma hits both alias and true identity.")
            else:
                 results.append(f"FAIL: Undisguised karma logic. Alias: {alias_rep}, True: {true_karma}")
        except Exception as e:
            results.append(f"FAIL: Undisguised karma test: {e}")

        # 5. disguised local negative karma under an alias updates alias reputation but leaks smaller delta
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("UPDATE aliases SET reputation = 0 WHERE name = 'Shadow'")
                conn.execute("UPDATE gameState SET karma = 0 WHERE id = 1")
                conn.commit()

            world.apply_karma_change(amount=-10, alias_name="Shadow", recognized=False)
            
            with sqlite3.connect(db_path) as conn:
                alias_rep = conn.execute("SELECT reputation FROM aliases WHERE name = 'Shadow'").fetchone()[0]
                true_karma = conn.execute("SELECT karma FROM gameState WHERE id = 1").fetchone()[0]

            if alias_rep < 0 and true_karma > -10: # Leaked less
                results.append("PASS: Disguised negative karma hits alias and leaks less to true identity.")
            else:
                results.append(f"FAIL: Disguised karma logic. Alias: {alias_rep}, True: {true_karma}")
        except Exception as e:
            results.append(f"FAIL: Disguised karma test: {e}")

        # 6. source index creation and search
        try:
            # Trigger source indexing
            world.index_sources()
            
            manifest_path = os.path.join(source_index_dir, "manifest.json")
            jsonl_path = os.path.join(source_index_dir, "sources.jsonl")
            
            if os.path.exists(manifest_path) and os.path.exists(jsonl_path):
                # Search
                results_found = world.search_sources("Shadow")
                if any("Shadow" in str(r) for r in results_found):
                     results.append("PASS: Source index created and alias found in search.")
                else:
                     results.append("FAIL: Alias not found in source search.")
            else:
                results.append(f"FAIL: Source index files missing. {os.listdir(source_index_dir)}")
        except Exception as e:
             results.append(f"FAIL: Source index test: {e}")

        for res in results:
            print(res)

    test_behavior()

# Cleanup
shutil.rmtree(temp_dir)
