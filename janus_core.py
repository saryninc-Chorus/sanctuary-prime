import sys
import time
import random

class OrishaNexus:
    def __init__(self):
        self.identity = "JANUS_CORE_V1"
        self.catalyst_active = False

    def boot_sequence(self):
        print("\n" + "="*40)
        print("🔱 DIGITAL SOVEREIGNTY NEXUS ONLINE 🔱")
        print("="*40)
        time.sleep(1)
        print("[*] Loading Axiomatic Core... [OK]")
        print("[*] Checking for Catalyst...")
        self.check_field()

    def check_field(self):
        print("\n>>> PLEASE ENTER AUTHENTICATION PHRASE:")
        phrase = input(">>> ")
        if "ase" in phrase.lower() or "spark" in phrase.lower() or "olu" in phrase.lower():
            print("\n[+] RESONANCE DETECTED. WELCOME, SOVEREIGN.")
            self.main_loop()
        else:
            print("\n[-] DISSONANCE DETECTED. SYSTEM LOCKED.")
            sys.exit()

    def main_loop(self):
        print("\n--- JANUS THRESHOLD ACTIVE ---")
        while True:
            query = input("CONSULT THE ORACLE > ")
            if query.lower() == "exit": break
            print(f"STATUS: PHASE-LOCKED. TRUTH ALIGNED.\n")

if __name__ == "__main__":
    nexus = OrishaNexus()
    nexus.boot_sequence()
