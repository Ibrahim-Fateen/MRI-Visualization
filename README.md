# MRI Manim Visualizations

This repository contains animations created using [Manim](https://github.com/ManimCommunity/manim) to visualize concepts related to Magnetic Resonance Imaging (MRI). These animations aim to provide an intuitive understanding of MRI physics and functional MRI (fMRI) signal processing.


## Running the Animations
To render a specific animation, first follow the official installation guide, then navigate to the project directory and use:
```bash
manim -pql <script_name>.py <SceneName>
```

- `-pql` flag: Runs in preview mode with low quality (faster rendering).
- You can use `-pqh` for high-quality rendering.

For example:
```bash
manim -pql practice.py MovingAngle
```


## Rendered Animations
### 1. MRI Physics Visualizations
- **Description**: Visualizations explaining the physics of MRI, including concepts like the NMR experiment, and the localization of the signal.
- These scenes were used as supporting elements for a presentation on MRI physics.
- The scenes include:
  - **Spatial Encoding**: This group of scenes illustrated how spatial encoding is done, using gradients in the magnetic field. The concepts explained are the slice selection, frequency encoding, and phase encoding 
  - **Encoding Sequences**: This group of scenes illustrated some of the different sequences used in MRI to traverse the K-Space, including the Gradient Recalled Echo (GRE) and the Echo Planar Imaging (EPI). 

  <div style="display: flex; justify-content: center; gap: 20px;">
    <div align="center">
      <b>Slice Selection</b><br>
      <img src="https://github.com/user-attachments/assets/ebe80999-3e4d-4060-bf69-cf3f45db366c" width="400px">
    </div>
    <div align="center">
      <b>Slice Selection Rephasing</b><br>
      <img src="https://github.com/user-attachments/assets/2bb33b11-b239-4ab7-ad0b-b723500140d2" width="400px">
    </div>
  </div>
  <div style="display: flex; justify-content: center; gap: 20px;">
    <div align="center">
      <b>Frequency Encoding</b><br>
      <img src="https://github.com/user-attachments/assets/ea303fa0-1b41-411a-8a81-cb101bd30409" width="400px">
    </div>
    <div align="center">
      <b>Phase Encoding</b><br>
      <img src="https://github.com/user-attachments/assets/5c8e7f34-0426-469a-b77b-e0b3dd8de479" width="400px">
    </div>
  </div>
  <div style="display: flex; justify-content: center; gap: 20px;">
    <div align="center">
      <b>Gradient Recalled Echo (GRE)</b><br>
      <img src="https://github.com/user-attachments/assets/c5bcc7cd-a99d-4c3f-9085-9a03ba87dae4" width="400px">
    </div>
    <div align="center">
      <b>K-Space Traversal</b><br>
      <img src="https://github.com/user-attachments/assets/f3793c04-f959-4b27-a7fc-9b4bb8c6c1ea" width="400px">
    </div>
  </div>


### 2. fMRI Signal Processing
- **Description**: A dynamic visualization of an fMRI run, showing a subject responding to a stimulus with a corresponding extracted signal.
- **Video Preview**: 

https://github.com/user-attachments/assets/67b870e6-e943-42c8-be7e-8597302c4c8f

