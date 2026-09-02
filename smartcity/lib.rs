use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn convert_to_grayscale(pixels: &mut [u8]) {
    let length = pixels.len();
    let mut i = 0;
    
    while i < length {
        let r = pixels[i] as f32;
        let g = pixels[i + 1] as f32;
        let b = pixels[i + 2] as f32;

        // Apply standard luminance formula
        let gray = (0.299 * r + 0.587 * g + 0.114 * b) as u8;

        pixels[i]     = gray; // Red
        pixels[i + 1] = gray; // Green
        pixels[i + 2] = gray; // Blue
        // pixels[i + 3] is Alpha (transparency) - left untouched

        i += 4;
    }
}