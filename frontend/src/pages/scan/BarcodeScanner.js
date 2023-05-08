import React, { Component } from "react";
import {
  BrowserMultiFormatReader,
  NotFoundException,
  BarcodeFormat,
} from "@zxing/library";
import ProductForm from "./ProductForm";

class BarcodeScanner extends Component {
  constructor(props) {
    super(props);

    this.state = {
      barcode: null,
      product: null,
      error: null,
      mode: true,
      isPlaying: false,
    };
  }

  async componentDidMount() {
    if (this.videoPlaying) {
      return;
    }

    try {
      // initialize barcode scanner
      const codeReader = new BrowserMultiFormatReader(null, {
        // Include EAN_13 and EAN_8 formats
        decodeFormats: [BarcodeFormat.EAN_13, BarcodeFormat.EAN_8],
      });
      const videoInputDevices = await codeReader.listVideoInputDevices();
      const selectedDeviceId = videoInputDevices[0].deviceId;
      const constraints = {
        video: {
          deviceId: {
            exact: selectedDeviceId,
          },
        },
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      const videoElement = document.getElementById("barcode-scanner");

      // check if video is already playing
      if (!this.videoPlaying) {
        videoElement.srcObject = stream;
        codeReader.decodeFromVideoDevice(
          selectedDeviceId,
          "barcode-scanner",
          (result, error) => {
            if (result) {
              this.handleBarcode(result.getText());
            } else if (error && !(error instanceof NotFoundException)) {
              console.error(error);
              this.setState({ error: "Failed to read barcode." });
            }
          }
        );
        this.handleBarcode("3017620422003");
        this.videoPlaying = true;
      }
    } catch (err) {
      this.setState({ error: "Failed to initialize barcode scanner." });
    }
  }

  handleBarcode = async (barcode) => {
    try {
      const response = await fetch(`http://localhost:4000/api/products/${barcode}`);
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      const p = await response.json();
      this.setState({ product: p, mode: "form" });
    } catch (error) {
      console.error(error);
      this.setState({ error: "Failed to retrieve product information." });
    }
  };

  onFormButtonClick = async (product) => {
    try {
      const response = await fetch(
        `http://localhost:4000/product/${product.barcode}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(product),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      this.setState({ product: null, mode: "video" });
    } catch (error) {
      console.error(error);
      this.setState({ error: "Failed to retrieve product information." });
    }
  };

  render() {
    const { product, mode } = this.state;
    return (
      <div>
        {mode === "video" ? (
          <video id="barcode-scanner" playsInline autoPlay muted />
        ) : (
          product && <ProductForm {...product} onFormButtonClick />
        )}
      </div>
    );
  }
}

export default BarcodeScanner;
