# hate-speech-detection

hate-speech-detection is a collection of exploratory scripts to train and predict hate speech in Polish text using machine learning.

It uses the [BAN-PL](https://github.com/ZILiAT-NASK/BAN-PL) dataset. Per its description, it is the "first publicly available dataset of offensive and harmful content banned from a web service Wykop.pl (often called the 'Polish Reddit') by professional moderators".

![A terminator holding an iPhone with angry emojis on its screen](/assets/hero.jpeg)

Image generated using OpenAI's [DALL-E 3](https://openai.com/dall-e-3).


## Motivation

For our final project in our university's AI course, we were tasked with developing a novel machine learning project. We decided to create a model that can identify hate speech within text. Given the prevalence of hate speech on social media platforms, we believe that such a model can have real-world applications and contribute positively to online interactions.


## Features

- Comprehensive documentation.
- TOML-based configuration system.


## Project Structure

The project is organized as follows:

- `configs`: Contains the configuration files for training various models.
- `datasets`: Contains the unpacked [BAN-PL](https://github.com/ZILiAT-NASK/BAN-PL) dataset as CSV files (after running the `prepare_datasets.py` script).
- `logs`: Contains the logs generated during training (after running any Python script).
- `models`: Contains the trained models (after running the `train.py` script).
- `modules`: Contains the [BAN-PL](https://github.com/ZILiAT-NASK/BAN-PL) dataset as a Git submodule.
- `scripts`: Contains Python scripts for training various models and running inference.


## Tested Systems

This project has been tested on the following systems:

- MacOS 14.4 (Sonoma)
<!-- - Manjaro 23.1 (Vulcan) -->


## Requirements

To run this project, you'll need:

- Python 3


## Setup

Follow these steps to setup the project:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/ryouze/hate-speech-detection.git
    ```

2. **Download the dataset**:

    To download the [BAN-PL](https://github.com/ZILiAT-NASK/BAN-PL) repository as a Git submodule, use the following commands:

    ```bash
    cd hate-speech-detection
    git submodule update --init --recursive
    ```

3. **Create a virtual environment (optional)**:

    ```bash
    mkdir -p ~/.local/env/
    python3 -m venv ~/.local/env/hate-speech-detection
    ```

    ```bash
    source ~/.local/env/hate-speech-detection/bin/activate
    ```

4. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Unpack the datasets**:

    Use the `prepare_datasets.py` script to prepare the datasets, storing the results as CSV files in the `datasets` directory.
    
    ```bash
    python3 scripts/prepare_datasets.py
    ```

After successful setup, you can proceed to the next section.


## Training the Model

To train the model, run the `train.py` script. You must pass the name of the config file as an argument (e.g., `debug.toml`). Optionally, you can include the `--verbose` flag to enable verbose logging. This will train the model on a down-stream task for classifying text as hate speech or not (it was originaly trained on a language modeling task). The trained model will be saved in the `models` directory.

```bash
python3 scripts/train.py debug.toml
```


## Running Inference

To classify text as hate speech or not, run:

```bash
python3 scripts/run.py
```


## Comparing Models

To compare the performance of different models, run:

```bash
python3 scripts/compare.py
```


## Contributing

All contributions are welcome.


## License

The original [BAN-PL](https://github.com/ZILiAT-NASK/BAN-PL) dataset is licensed under the CC-BY-4.0 License. A copy of the license is included in this repository. Please see the [LICENSE](LICENSE) file for more details.
