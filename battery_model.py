class BatteryModel:
    def __init__(self, capacity_kwh=100, initial_soc=0.2, ambient_temp=25):
        # Battery parameters
        self.capacity = capacity_kwh * 3600 * 1000  # Convert to Joules
        self.soc = initial_soc  # State of Charge (0-1)
        self.voltage = 350  # Nominal voltage (V)
        self.temperature = ambient_temp  # °C
        self.ambient_temp = ambient_temp
        self.thermal_mass = 20000  # J/°C
        self.heat_coeff = 0.001  # Heat generation coefficient
        self.cooling_coeff = 0.005  # Cooling coefficient
        
    def efficiency(self):
        """Calculate charging efficiency based on SOC and temperature"""
        soc_factor = 0.95 * (1 - self.soc**2)  # Efficiency drops as SOC increases
        temp_factor = 1 - 0.0005 * (self.temperature - 25)**2  # Ideal at 25°C
        return max(0.7, min(0.98, soc_factor * temp_factor))
    
    def charge(self, power_w, dt):
        """Charge the battery for time dt (seconds)"""
        # Calculate actual power considering efficiency
        eff = self.efficiency()
        actual_power = power_w * eff
        
        # Calculate energy added to battery
        energy_added = actual_power * dt
        
        # Calculate heat generated
        heat_generated = power_w * (1 - eff) * dt
        
        # Update SOC
        self.soc = min(1.0, self.soc + energy_added / self.capacity)
        
        # Update temperature
        self.temperature += heat_generated / self.thermal_mass
        # Cooling effect proportional to temperature difference
        self.temperature -= self.cooling_coeff * (self.temperature - self.ambient_temp) * dt
        
        # Update voltage based on SOC
        self.voltage = 250 + 150 * self.soc - 50 * (1 - self.soc)**2
        
        # Return metrics for monitoring
        return {
            'soc': self.soc * 100,
            'temperature': self.temperature,
            'voltage': self.voltage,
            'efficiency': eff * 100,
            'power_in': power_w
        }