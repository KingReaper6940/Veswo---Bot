#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::CustomMenuItem;
use reqwest;
use serde_json::json;

#[tauri::command]
async fn chat(message: String) -> Result<String, String> {
    let client = reqwest::Client::new();
    let res = client
        .post("http://localhost:8000/api/chat")
        .json(&json!({ "message": message }))
        .send()
        .await
        .map_err(|e| e.to_string())?;

    if !res.status().is_success() {
        return Err(format!("Backend error: {}", res.status()));
    }

    let json: serde_json::Value = res.json().await.map_err(|e| e.to_string())?;
    let response = json.get("response").cloned().unwrap_or(json!("No response found")).to_string();
    Ok(response)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![chat])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
} 