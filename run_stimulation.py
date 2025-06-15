from stimulation_gui import interactive, create_gui, BatterySimulation
from battery_model import BatteryModel
import sys

def run_direct_simulation():
    """Run simulation with specific parameters without GUI"""
    sim = BatterySimulation()
    
    # Set custom parameters
    initial_soc = 0.2      # 20%
    ambient_temp = 45      # 45°C (hot environment)
    charging_mode = 'Supercharger'
    minutes = 30           # 30-minute simulation
    
    print(f"\nRunning simulation with:")
    print(f"  Initial SOC: {initial_soc*100}%")
    print(f"  Ambient Temp: {ambient_temp}°C")
    print(f"  Charging Mode: {charging_mode}")
    print(f"  Duration: {minutes} minutes\n")
    
    sim.model = BatteryModel(
        initial_soc=initial_soc,
        ambient_temp=ambient_temp
    )
    sim.simulate_charging(charging_mode, total_minutes=minutes)

if __name__ == "__main__":
    if interactive:
        # Show GUI only in interactive mode (local machine)
        create_gui()
    else:
        # Run directly in non-interactive mode (Codespace)
        run_direct_simulation()
