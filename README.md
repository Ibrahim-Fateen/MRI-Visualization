# MRI Manim Visualizations

This repository contains animations created using [Manim](https://github.com/ManimCommunity/manim) to visualize concepts related to Magnetic Resonance Imaging (MRI). These animations aim to provide an intuitive understanding of MRI physics and functional MRI (fMRI) signal processing.


## Running the Animations
To render a specific animation, first follow the official installation guide, then navigate to the project directory and use:
```bash
manim -pql <script_name>.py
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
- Work in progress.

[//]: # (- **Video Preview**: ![MRI Physics]&#40;videos/mri_physics.gif&#41;)

### 2. fMRI Signal Processing
- **Description**: A dynamic visualization of an fMRI run, showing a subject responding to a stimulus with a corresponding extracted signal.
- **Video Preview**: 
