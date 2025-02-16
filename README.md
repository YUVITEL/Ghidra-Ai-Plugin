# Ghidra AI Plugin - Advanced Deobfuscation With AI

## 🚀 Overview
The **Ghidra AI Plugin** is an advanced AI-assisted tool designed to analyze obfuscated functions within Ghidra, attempt decompilation, and convert them into readable, understandable code using AI models.

🔹 Uses **threading** for faster processing.  
🔹 Enhances **code readability** and **reverse engineering** efficiency.  
🔹 Designed for **educational and research purposes only**.

---

## 📌 Features
- **Function-Level Scanning**: Analyzes each function independently.
- **AI-Powered Deobfuscation**: Uses AI models to translate obfuscated code into readable format.
- **Multi-Threading**: Boosts performance by parallelizing function decompilation.
- **Seamless Ghidra Integration**: Works directly within Ghidra's analysis workflow.
- **Supports Multiple Architectures**: Can process various assembly and machine code formats.

---

## 🛠 Installation

### Prerequisites
Ensure you have the following installed:
- [Ghidra](https://ghidra-sre.org/)

### Steps
1. **Copy the code**:
   ```sh
   https://raw.githubusercontent.com/Subhashis360/Ghidra-Ai-Plugin/refs/heads/main/aiscanner.py
   ```

---

## ▶️ Usage
1. **Open Ghidra** and load the binary.
2. **Run the AI Plugin**:
   - Go to **Windows > Script Manager** in Ghidra.
   - Click the **Add Script** button in the upper section.
   - add a name of the script and done.
   - Paste the `aiscanner.py` code.
   - Click **Run** to execute it.
3. **View Deobfuscated Code**:
   - The plugin scans each function and attempts to decompile it.
   - Outputs will come each funtion starting as a comment .

---

## ⚠️ Disclaimer
This tool is for **educational and research purposes only**. Misuse for unethical or illegal activities is strictly prohibited.

---

## 📜 License
MIT License - Free to use, modify, and distribute with attribution.

---

## 📩 Contributing
Pull requests and suggestions are welcome! Open an issue to discuss improvements.

---

## 🔗 Contact
For questions, reach out via GitHub Issues.

---

### 🌟 Star this repository if you find it useful!

