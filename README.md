
#MAT187 MINI-PROJECT
#Smart EV Battery Life Simulator 
#“Modeling and Simulation of Electric Vehicle Battery Performance” 


#Features of this Simulation: 

1. Realistic Battery Physics: 

   - State of Charge (SOC) calculation 

   - Temperature-dependent efficiency 

   - Internal resistance modeling 

   - Voltage curve simulation 

   - Thermal management system 

 

2. Multiple Charging Modes: 

   - Level 1 Home Charging (1.8 kW) 

   - Level 2 Home Charging (7.2 kW) 

   - Supercharger (150 kW) 

 

3. Real-Time Visualization: 

   - Live updating graphs of SOC, temperature, efficiency 

   - Voltage and power monitoring 

   - Animated progress (1 sec = 1 min of charging) 

 

4. Interactive GUI: 

   - Adjustable initial SOC (0-100%) 

   - Ambient temperature control (-10°C to 40°C) 

   - Charging mode selection 

 

5. Advanced Battery Behavior: 

   - Efficiency decreases as SOC approaches 100% 

   - Temperature affects charging performance 

   - Cooling system simulation 

   - Non-linear voltage curve 

 

#Core Libraries Used: 

1. NumPy - For numerical computations 

2. Matplotlib - For creating visualizations and plots 

3. Matplotlib Widgets - For interactive GUI elements 

4. Matplotlib Animation - For real-time updating graphs 

 

#How to Use: 

For CodeSpace- 

LINK- Github link For Stimulation 

1. Run command in terminal- Example 
python run_stimulation.py --soc 40 --temp 10 --mode "Home Plug (L2)" --minutes 45 

2. Run the program to launch the configuration GUI 

3. Set your desired initial SOC and ambient temperature 

4. Select a charging mode 

5. Watch as the battery charges with live-updating graphs 

 

The simulation shows how charging speed, efficiency, and temperature change throughout the charging process, with superchargers heating the battery more than slower home charging. The visualization updates every second, representing one minute of charging time. 

 

What You'll See: 

1. First write the command

   - SOC slider (0-100%) 

   - Temperature slider (-10°C to 40°C) 

   - Charging mode selector 

 

2. After entering, you'll see: 

   - Real-time updating graphs 

   - Top plot: SOC %, Temperature, Efficiency 

   - Bottom plot: Voltage, Power Input 

   - Live-updating values (1 second = 1 minute of charging) 

 

The simulation models realistic battery behavior: 

- Charging slows down as battery fills 

- Efficiency drops at high SOC 

- Temperature affects performance 

- Different charging modes (home vs supercharger) 

- Voltage curve follows real battery characteristics 
