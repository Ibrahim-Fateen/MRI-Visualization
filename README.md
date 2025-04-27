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
  - **Encoding Sequences**: This group of scenes illustrated some of the different sequences used in MRI to traverse the K-Space, including the GRE, and the EPI. 

[//]: # (- **Video Preview**: ![MRI Physics]&#40;videos/mri_physics.gif&#41;)

### 2. fMRI Signal Processing
- **Description**: A dynamic visualization of an fMRI run, showing a subject responding to a stimulus with a corresponding extracted signal.
- **Video Preview**: 

https://github.com/user-attachments/assets/67b870e6-e943-42c8-be7e-8597302c4c8f


