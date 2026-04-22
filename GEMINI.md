# GEMINI.md - Project Context & Instructions

This document provides essential context and instructions for AI agents working on the `matplotlib_GraphPad_style` repository.

## 📌 Project Overview
A collection of custom `matplotlib` styles specifically designed for the medical and biological sciences, mimicking the aesthetic of **GraphPad Prism** and other professional scientific plotting tools (e.g., **DeepTools**).

- **Core Technologies:** Python, Matplotlib, NumPy, SciPy, Scikit-learn.
- **Main Goal:** Standardize high-quality, publication-ready scientific charts with minimal manual formatting.

## 📁 Directory Structure
The project follows a strict modular structure under the `styles/` directory:
- `styles/<style_name>/`:
    - `assets/`: Contains the `.mplstyle` configuration file.
    - `img/`: Contains example outputs (`.png`, `.pdf`).
    - `example.py`: A self-contained script to reproduce the chart using mock data.
    - `readme.md`: Specific documentation and visual preview for the style.
- `scripts/`: Utility scripts, such as `new_style.sh` for scaffolding.

## 🛠️ Development Workflow

### Building & Running
1. **Environment Setup:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Generating Examples:**
   Navigate to a style directory and run:
   ```bash
   python example.py
   ```
3. **Adding a New Style:**
   Use the scaffolding script:
   ```bash
   ./scripts/new_style.sh <your_style_name>
   ```

### Coding Conventions (Mandatory)
1. **Path Management:** Always use `pathlib.Path` for file resolution. Avoid hardcoded strings.
   ```python
   from pathlib import Path
   root_path = Path(__file__).parent
   style_file = root_path / 'assets/style.mplstyle'
   ```
2. **Style Application:** Load the `.mplstyle` file **before** creating any figure or axis objects.
   ```python
   plt.style.use(style_file)
   ```
3. **Script Structure:** Use a `main()` function and type hints.
   ```python
   def plot_data(data: np.ndarray): ...
   def main(): ...
   if __name__ == '__main__': main()
   ```
4. **GraphPad Aesthetics:**
    - Prefer bold fonts for labels and titles (`font.weight: bold`).
    - Hide top and right spines.
    - Use inward-facing, thick tick marks.
    - For biological data, prefer asymmetric error bars (upper only).

## 🤖 AI specific Instructions (from llms.md)
- **Prioritize `.mplstyle`:** Rely on the style sheet for global parameters rather than redundant code in `example.py`.
- **Reproducibility:** Ensure `example.py` generates both `.png` and `.pdf` in the `img/` folder.
- **Contribution:** When creating a new style, strictly follow the folder structure defined in `CONTRIBUTING.md`.

## 🤝 Contribution Guidelines
Refer to `CONTRIBUTING.md` for detailed PR requirements. Any new style must include a `readme.md` with an embedded preview of the result image.
