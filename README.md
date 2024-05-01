# Grapes segmentation

This project demonstrates the segmentation of grape images  in real-time.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/VVebSharE/DLHackWeb
    ```

2. Navigate to the project directory:

    ```bash
    cd DLHackWeb
    ```

3. Install the required Python packages using pip:

    ```bash
    pip install -r req.txt
    ```

4. Create a `.env` file in the project root directory and add your JWT secret key:

    ```plaintext
    JWT_SECRET_KEY=your_secret_key_here
    ```

5. Update in inferece.py to add the path of the model file.

    ```
    from PIDNET_UPDATed.tools.custommy import Model #change this import to your model
    mymodel = Model()
    ```


## Usage

To run the Flask application, execute the following command:

```bash
flask run
```

To run on local network:

```bash
flask run --host=0.0.0.0
```

## Integrate your Frontend

Update the request url in the frontend to the url of the backend server.

