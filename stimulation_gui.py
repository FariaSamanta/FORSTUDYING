import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons
from battery_model import BatteryModel

def simulate_charging(model, charging_mode, total_minutes=120):
    """Simulate battery charging with real-time visualization"""
    # Setup figure and subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('EV Battery Charging Simulation', fontsize=16)
    plt.subplots_adjust(hspace=0.4)
    
    # Set charging power based on mode (Watts)
    power_levels = {
        'Home Plug (L1)': 1800, 
        'Home Plug (L2)': 7200,
        'Supercharger': 150000
    }
    power = power_levels[charging_mode]
    
    # Initialize data storage
    times = [0]
    socs = [model.soc * 100]
    temps = [model.temperature]
    volts = [model.voltage]
    effs = [model.efficiency() * 100]
    
    # Create plots
    line_soc, = ax1.plot(times, socs, 'b-', label='SOC (%)')
    line_temp, = ax1.plot(times, temps, 'r-', label='Temp (°C)')
    line_eff, = ax1.plot(times, effs, 'g-', label='Efficiency (%)')
    ax1.set_title('State of Charge, Temperature and Efficiency')
    ax1.set_xlabel('Time (minutes)')
    ax1.set_ylabel('Value')
    ax1.legend(loc='upper left')
    ax1.grid(True)
    ax1.set_ylim(0, 100)
    
    line_voltage, = ax2.plot(times, volts, 'm-', label='Voltage (V)')
    ax2.set_title('Voltage')
    ax2.set_xlabel('Time (minutes)')
    ax2.set_ylabel('Voltage (V)')
    ax2.legend(loc='upper left')
    ax2.grid(True)
    ax2.set_ylim(200, 400)
    
    # Add text annotations
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)
    power_text = ax1.text(0.02, 0.85, f'Power: {power/1000:.1f} kW | SOC: {socs[-1]:.1f}%', transform=ax1.transAxes)
    mode_text = ax1.text(0.02, 0.75, f'Mode: {charging_mode}', transform=ax1.transAxes)
    
    # Animation update function
    def update(frame):
        # Charge for 1 minute (60 seconds)
        metrics = model.charge(power, 60)
        
        # Record data
        times.append(times[-1] + 1)
        socs.append(metrics['soc'])
        temps.append(metrics['temperature'])
        volts.append(metrics['voltage'])
        effs.append(metrics['efficiency'])
        
        # Update plots
        line_soc.set_data(times, socs)
        line_temp.set_data(times, temps)
        line_eff.set_data(times, effs)
        line_voltage.set_data(times, volts)
        
        # Update axes limits
        ax1.set_xlim(0, max(10, times[-1] + 5))
        ax2.set_xlim(0, max(10, times[-1] + 5))
        
        # Update text
        time_text.set_text(f'Time: {times[-1]} min')
        power_text.set_text(f'Power: {power/1000:.1f} kW | SOC: {socs[-1]:.1f}%')
        
        return (line_soc, line_temp, line_eff, line_voltage, 
                time_text, power_text)
    
    # Create animation (1 frame per second = 1 minute of charging)
    ani = FuncAnimation(fig, update, frames=total_minutes, 
                        interval=1000, blit=False)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def create_gui():
    """Create a GUI for setting simulation parameters"""
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.1, bottom=0.4)
    ax.set_title('EV Battery Charging Simulator - Configure Parameters')
    ax.axis('off')
    
    # Create sliders
    ax_soc = plt.axes([0.25, 0.25, 0.65, 0.03])
    ax_temp = plt.axes([0.25, 0.20, 0.65, 0.03])
    
    soc_slider = Slider(ax_soc, 'Initial SOC (%)', 0, 100, valinit=20, valstep=1)
    temp_slider = Slider(ax_temp, 'Ambient Temp (°C)', -10, 40, valinit=25, valstep=1)
    
    # Create radio buttons for charging mode
    rax = plt.axes([0.25, 0.05, 0.65, 0.10])
    radio = RadioButtons(rax, ('Home Plug (L1)', 'Home Plug (L2)', 'Supercharger'), active=0)
    
    # Create start button
    ax_button = plt.axes([0.35, 0.30, 0.3, 0.05])
    button = Button(ax_button, 'Start Simulation', color='lightblue')
    
    # Button click handler
    def start_simulation(event):
        plt.close(fig)
        model = BatteryModel(initial_soc=soc_slider.val/100, 
                            ambient_temp=temp_slider.val)
        simulate_charging(model, radio.value_selected)
    
    button.on_clicked(start_simulation)
    
    plt.show()