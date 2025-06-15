import argparse
import sys
from stimulation_gui import interactive, BatterySimulation
from battery_model import BatteryModel

def run_simulation_from_args(args):
    """Run simulation with command-line parameters"""
    sim = BatterySimulation()
    sim.model = BatteryModel(
        initial_soc=args.soc/100.0,  # Convert percentage to fraction
        ambient_temp=args.temp
    )
    sim.simulate_charging(args.mode, total_minutes=args.minutes)

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Run EV Battery Charging Simulation')
    
    parser.add_argument('--soc', type=float, default=20.0, 
                        help='Initial State of Charge (percentage) [0-100]')
    parser.add_argument('--temp', type=float, default=25.0, 
                        help='Ambient Temperature (°C) [-10 to 40]')
    parser.add_argument('--mode', type=str, default='Supercharger', 
                        choices=['Home Plug (L1)', 'Home Plug (L2)', 'Supercharger'],
                        help='Charging mode')
    parser.add_argument('--minutes', type=int, default=30, 
                        help='Simulation duration in minutes')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not 0 <= args.soc <= 100:
        print("Error: SOC must be between 0 and 100")
        sys.exit(1)
    if not -10 <= args.temp <= 40:
        print("Error: Temperature must be between -10°C and 40°C")
        sys.exit(1)
    
    print(f"Starting simulation with:")
    print(f"  Initial SOC: {args.soc}%")
    print(f"  Ambient Temperature: {args.temp}°C")
    print(f"  Charging Mode: {args.mode}")
    print(f"  Duration: {args.minutes} minutes\n")
    
    if interactive and not any(sys.argv[1:]):
        # Show GUI if in interactive mode and no arguments provided
        from stimulation_gui import create_gui
        create_gui()
    else:
        # Run with command-line parameters
        run_simulation_from_args(args)