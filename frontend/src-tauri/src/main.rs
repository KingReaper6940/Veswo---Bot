#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::{CustomMenuItem, Manager};
use reqwest;
use serde_json::json;
use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;
use std::path::Path;

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

fn start_backend() -> std::process::Child {
    // Get the app directory
    let exe_path = std::env::current_exe()
        .expect("Failed to get executable path");
    let app_dir = exe_path
        .parent()
        .expect("Failed to get executable directory")
        .parent()
        .expect("Failed to get app directory")
        .parent()
        .expect("Failed to get app bundle directory");
    
    // Check if we're in development mode (running from project directory)
    let dev_launcher = Path::new("launcher.sh");
    let launcher_path = if dev_launcher.exists() {
        dev_launcher.to_path_buf()
    } else {
        app_dir.join("launcher.sh")
    };
    
    println!("Starting backend with launcher: {:?}", launcher_path);
    
    // Start the backend using the launcher script
    let backend_process = Command::new("bash")
        .arg(launcher_path)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("Failed to start backend server");
    
    // Wait a moment for the server to start
    thread::sleep(Duration::from_secs(5));
    
    backend_process
}

fn main() {
    // Start the backend server in a separate thread
    let backend_handle = thread::spawn(|| {
        let mut backend_process = start_backend();
        println!("Backend server started with PID: {}", backend_process.id());
        
        // Keep the backend running
        let _ = backend_process.wait();
    });
    
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![chat])
        .setup(|app| {
            println!("veswo1-bot starting...");
            println!("Backend server should be running on http://localhost:8000");
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
} 