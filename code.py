#!/usr/bin/env python3
"""
Transducer Power Controller
Controls a transducer w-s count with user-defined power settings
"""

import time
import threading
from typing import Optional

class TransducerController:
    def __init__(self):
        self.MIN_POWER = 50      # Minimum power setting (w-s)
        self.MAX_POWER = 5000    # Maximum power setting (w-s)
        self.current_power = 0   # Current power level
        self.target_power = 0    # Target power to stop at
        self.is_running = False  # Transducer running state
        self.stop_event = threading.Event()
        
    def validate_power_setting(self, power: float) -> bool:
        """Validate if the power setting is within allowed range"""
        return self.MIN_POWER <= power <= self.MAX_POWER
    
    def get_user_power_setting(self) -> Optional[float]:
        """Get and validate power setting from user input"""
        while True:
            try:
                power_input = input(f"\nEnter desired power setting ({self.MIN_POWER}-{self.MAX_POWER} w-s) or 'q' to quit: ")
                
                if power_input.lower() == 'q':
                    return None
                
                power = float(power_input)
                
                if self.validate_power_setting(power):
                    return power
                else:
                    print(f"Error: Power setting must be between {self.MIN_POWER} and {self.MAX_POWER} w-s")
                    
            except ValueError:
                print("Error: Please enter a valid number")
    
    def simulate_transducer_operation(self):
        """Simulate transducer operation with increasing power"""
        print(f"Starting transducer operation...")
        print(f"Target power: {self.target_power} w-s")
        print("-" * 40)
        
        # Simulate power ramping up
        power_increment = 10  # w-s per step
        delay = 0.1  # seconds between increments
        
        self.current_power = 0
        self.is_running = True
        
        while self.is_running and self.current_power < self.target_power:
            if self.stop_event.is_set():
                break
                
            self.current_power += power_increment
            
            # Don't exceed target power
            if self.current_power > self.target_power:
                self.current_power = self.target_power
            
            # Display current status
            print(f"Current power: {self.current_power:6.1f} w-s", end='\r')
            
            time.sleep(delay)
        
        # Stop transducer
        self.stop_transducer()
    
    def stop_transducer(self):
        """Stop the transducer operation"""
        self.is_running = False
        print(f"\n{'='*40}")
        print(f"TRANSDUCER STOPPED at {self.current_power} w-s")
        print(f"Target power reached: {self.current_power >= self.target_power}")
        print(f"{'='*40}")
    
    def emergency_stop(self):
        """Emergency stop function"""
        print("\nEMERGENCY STOP ACTIVATED!")
        self.stop_event.set()
        self.stop_transducer()
    
    def run(self):
        """Main program loop"""
        print("=" * 50)
        print("    TRANSDUCER POWER CONTROLLER")
        print("=" * 50)
        print(f"Power Range: {self.MIN_POWER} - {self.MAX_POWER} w-s")
        print("Press Ctrl+C for emergency stop")
        
        try:
            while True:
                # Reset stop event
                self.stop_event.clear()
                
                # Get user input for power setting
                target_power = self.get_user_power_setting()
                
                if target_power is None:
                    print("Exiting program...")
                    break
                
                self.target_power = target_power
                
                # Start transducer operation in a separate thread
                operation_thread = threading.Thread(
                    target=self.simulate_transducer_operation
                )
                operation_thread.daemon = True
                operation_thread.start()
                
                # Wait for operation to complete
                operation_thread.join()
                
                # Ask if user wants to continue
                continue_choice = input("\nDo you want to run another cycle? (y/n): ")
                if continue_choice.lower() != 'y':
                    break
                    
        except KeyboardInterrupt:
            print("\n" + "="*50)
            print("EMERGENCY STOP - Program terminated by user")
            self.emergency_stop()
        
        print("Program ended.")

def main():
    """Main function"""
    controller = TransducerController()
    controller.run()

if __name__ == "__main__":  
    main()
