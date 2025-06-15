import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons
from battery_model import BatteryModel

# Detect environment and set backend
is_codespace = 'CODESPACE_NAME' in os.environ or 'CODESPACES' in os.environ
has_display = 'DISPLAY' in os.environ and os.environ['DISPLAY']

if is_codespace or not has_display:
    matplotlib.use('TKAgg')  # Non-interactive for Codespaces
    interactive = False
    print("Running in non-interactive mode (Codespace)")
else:
    matplotlib.use('TkAgg')  # Interactive for local machines
    interactive = True
    print("Running in interactive mode (Local)")

class BatterySimulation:
    def __init__(self):
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.line_soc = None
        self.line_temp = None
        self.line_eff = None
        self.line_voltage = None
        self.time_text = None
        self.power_text = None
        self.mode_text = None
        self.model = None
        self.charging_mode = None
        self.ani = None
        self.annot_soc = None
        self.annot_temp = None
        self.annot_eff = None
        self.annot_voltage = None
        self.interactive = interactive
        self.output_dir = "simulation_frames"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def simulate_charging(self, charging_mode, total_minutes=120):
        """Simulate battery charging with real-time visualization or frame saving"""
        # Create output directory
        if not self.interactive:
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"Saving frames to directory: {self.output_dir}/")
        
        # Setup figure and subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 10))
        self.fig.suptitle('EV Battery Charging Simulation', fontsize=16)
        plt.subplots_adjust(hspace=0.4)
        
        # Set charging power based on mode (Watts)
        power_levels = {
            'Home Plug (L1)': 1800, 
            'Home Plug (L2)': 7200,
            'Supercharger': 150000
        }
        power = power_levels[charging_mode]
        self.charging_mode = charging_mode
        
        # Initialize data storage
        self.times = [0]
        self.socs = [self.model.soc * 100]
        self.temps = [self.model.temperature]
        self.volts = [self.model.voltage]
        self.effs = [self.model.efficiency() * 100]
        
        # Create plots with markers
        self.line_soc, = self.ax1.plot(self.times, self.socs, 'b-', label='SOC (%)', marker='o', markersize=4)
        self.line_temp, = self.ax1.plot(self.times, self.temps, 'r-', label='Temp (°C)', marker='s', markersize=4)
        self.line_eff, = self.ax1.plot(self.times, self.effs, 'g-', label='Efficiency (%)', marker='^', markersize=4)
        self.ax1.set_title('State of Charge, Temperature and Efficiency')
        self.ax1.set_xlabel('Time (minutes)')
        self.ax1.set_ylabel('Value')
        
        # Position legend in upper right to avoid overlapping
        self.ax1.legend(loc='upper right')
        self.ax1.grid(True)
        self.ax1.set_ylim(0, 100)
        
        self.line_voltage, = self.ax2.plot(self.times, self.volts, 'm-', label='Voltage (V)', marker='d', markersize=4)
        self.ax2.set_title('Voltage')
        self.ax2.set_xlabel('Time (minutes)')
        self.ax2.set_ylabel('Voltage (V)')
        self.ax2.legend(loc='upper right')  # Position legend in upper right
        self.ax2.grid(True)
        self.ax2.set_ylim(200, 400)
        
        # Add text annotations in lower left with backgrounds
        self.time_text = self.ax1.text(0.02, 0.05, '', transform=self.ax1.transAxes,
                                      bbox=dict(facecolor='white', alpha=0.7, boxstyle="round,pad=0.3"))
        self.power_text = self.ax1.text(0.02, 0.15, f'Power: {power/1000:.1f} kW | SOC: {self.socs[-1]:.1f}%', 
                                       transform=self.ax1.transAxes,
                                       bbox=dict(facecolor='white', alpha=0.7, boxstyle="round,pad=0.3"))
        self.mode_text = self.ax1.text(0.02, 0.25, f'Mode: {charging_mode}', 
                                      transform=self.ax1.transAxes,
                                      bbox=dict(facecolor='white', alpha=0.7, boxstyle="round,pad=0.3"))
        
        # Initialize point annotations
        self.annot_soc = self.ax1.annotate('', xy=(0,0), xytext=(5,5), textcoords='offset points',
                                          bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", alpha=0.7))
        self.annot_temp = self.ax1.annotate('', xy=(0,0), xytext=(5,5), textcoords='offset points',
                                           bbox=dict(boxstyle="round,pad=0.3", fc="lightcoral", alpha=0.7))
        self.annot_eff = self.ax1.annotate('', xy=(0,0), xytext=(5,5), textcoords='offset points',
                                          bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen", alpha=0.7))
        self.annot_voltage = self.ax2.annotate('', xy=(0,0), xytext=(5,5), textcoords='offset points',
                                              bbox=dict(boxstyle="round,pad=0.3", fc="plum", alpha=0.7))
        
        # Hide annotations initially
        self.annot_soc.set_visible(False)
        self.annot_temp.set_visible(False)
        self.annot_eff.set_visible(False)
        self.annot_voltage.set_visible(False)
        
        # Create animation
        self.ani = FuncAnimation(self.fig, self.update, frames=total_minutes, 
                                interval=1000 if self.interactive else 100, 
                                blit=False)
        
        # Run the animation
        if self.interactive:
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()
        else:
            # In non-interactive mode, we need to run the animation to completion
            for frame in range(total_minutes):
                self.update(frame)
                if frame % 5 == 0:  # Print progress every 5 frames
                    progress = (frame + 1) / total_minutes * 100
                    print(f"Simulating... {progress:.1f}% complete")
            
            # Save final state
            final_image = f"final_state_{self.timestamp}.png"
            self.fig.savefig(os.path.join(self.output_dir, final_image))
            print(f"Final state saved to {self.output_dir}/{final_image}")
            
            # Create video from frames
            self.create_video(total_minutes)
            
            # Clean up
            plt.close(self.fig)

    def update(self, frame):
        """Animation update function"""
        # Set charging power based on mode
        power_levels = {
            'Home Plug (L1)': 1800, 
            'Home Plug (L2)': 7200,
            'Supercharger': 150000
        }
        power = power_levels[self.charging_mode]
        
        # Charge for 1 minute (60 seconds)
        metrics = self.model.charge(power, 60)
        
        # Record data
        self.times.append(self.times[-1] + 1)
        self.socs.append(metrics['soc'])
        self.temps.append(metrics['temperature'])
        self.volts.append(metrics['voltage'])
        self.effs.append(metrics['efficiency'])
        
        # Update plots
        self.line_soc.set_data(self.times, self.socs)
        self.line_temp.set_data(self.times, self.temps)
        self.line_eff.set_data(self.times, self.effs)
        self.line_voltage.set_data(self.times, self.volts)
        
        # Update axes limits
        self.ax1.set_xlim(0, max(10, self.times[-1] + 5))
        self.ax2.set_xlim(0, max(10, self.times[-1] + 5))
        
        # Update text
        self.time_text.set_text(f'Time: {self.times[-1]} min')
        self.power_text.set_text(f'Power: {power/1000:.1f} kW | SOC: {self.socs[-1]:.1f}%')

        # Add overheating warning if applicable
        if metrics['power_in'] == 0:
            warning_text = "⚠️ CHARGING STOPPED: Overheating! ⚠️"
            # Create or update warning text
            if not hasattr(self, 'warning_text'):
                self.warning_text = self.ax1.text(0.5, 0.5, warning_text, 
                                                 transform=self.ax1.transAxes,
                                                 fontsize=20, color='red',
                                                 ha='center', va='center',
                                                 bbox=dict(facecolor='yellow', alpha=0.8))
            else:
                self.warning_text.set_text(warning_text)
        # If charging is not stopped, remove the warning if it exists
        elif hasattr(self, 'warning_text'):
            self.warning_text.set_visible(False)
        
        # Update point annotations
        self._update_annotations()
        
        # Save frame if in non-interactive mode
        if not self.interactive:
            frame_file = os.path.join(self.output_dir, f"frame_{frame:04d}.png")
            self.fig.savefig(frame_file)
        
        return (self.line_soc, self.line_temp, self.line_eff, self.line_voltage, 
                self.time_text, self.power_text)
    
    def _update_annotations(self):
        """Update the data point annotations"""
        # Update and show annotations for the latest point
        x = self.times[-1]
        
        # SOC annotation
        self.annot_soc.xy = (x, self.socs[-1])
        self.annot_soc.set_text(f'SOC: {self.socs[-1]:.1f}%')
        self.annot_soc.set_visible(True)
        
        # Temperature annotation
        self.annot_temp.xy = (x, self.temps[-1])
        self.annot_temp.set_text(f'Temp: {self.temps[-1]:.1f}°C')
        self.annot_temp.set_visible(True)
        
        # Efficiency annotation
        self.annot_eff.xy = (x, self.effs[-1])
        self.annot_eff.set_text(f'Eff: {self.effs[-1]:.1f}%')
        self.annot_eff.set_visible(True)
        
        # Voltage annotation
        self.annot_voltage.xy = (x, self.volts[-1])
        self.annot_voltage.set_text(f'Volt: {self.volts[-1]:.1f}V')
        self.annot_voltage.set_visible(True)
        
        # Adjust positions to prevent overlap
        self.annot_soc.xyann = (10, 0)
        self.annot_temp.xyann = (10, -25)
        self.annot_eff.xyann = (10, 25)
        self.annot_voltage.xyann = (10, 0)
    
    def create_video(self, total_frames):
        """Create video from saved frames using ffmpeg"""
        try:
            video_file = f"battery_simulation_{self.timestamp}.mp4"
            cmd = f"ffmpeg -framerate 1 -i {self.output_dir}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p {video_file}"
            os.system(cmd)
            
            if os.path.exists(video_file):
                print(f"Video created successfully: {video_file}")
                print(f"File size: {os.path.getsize(video_file)/1024:.1f} KB")
            else:
                print("Video creation failed. Please check if ffmpeg is installed.")
        except Exception as e:
            print(f"Error creating video: {e}")

def create_gui():
    """Create a GUI for setting simulation parameters"""
    sim = BatterySimulation()
    
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
        sim.model = BatteryModel(initial_soc=soc_slider.val/100, 
                                ambient_temp=temp_slider.val)
        sim.simulate_charging(radio.value_selected, total_minutes=120)  # Shorter for testing
    
    button.on_clicked(start_simulation)
    
    plt.show()