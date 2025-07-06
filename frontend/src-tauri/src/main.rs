#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use reqwest;
use serde_json::json;
use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;
use std::path::Path;
use tauri::{Manager, RunEvent, WindowEvent, Window};
use std::sync::{Arc, Mutex};

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

#[tauri::command]
async fn set_glass_mode(window: Window, enable: bool) -> Result<(), String> {
    if enable {
        window.set_decorations(false).map_err(|e| e.to_string())?;
        window.set_transparent(true).map_err(|e| e.to_string())?;
        window.set_size(tauri::Size::Logical(tauri::LogicalSize { width: 350.0, height: 180.0 })).map_err(|e| e.to_string())?;
        window.set_always_on_top(true).map_err(|e| e.to_string())?;
    } else {
        window.set_decorations(true).map_err(|e| e.to_string())?;
        window.set_transparent(false).map_err(|e| e.to_string())?;
        window.set_size(tauri::Size::Logical(tauri::LogicalSize { width: 1200.0, height: 800.0 })).map_err(|e| e.to_string())?;
        window.set_always_on_top(false).map_err(|e| e.to_string())?;
    }
    Ok(())
}

fn start_ollama() -> Option<std::process::Child> {
    // Check if ollama is already running
    if let Ok(output) = Command::new("pgrep").arg("ollama").output() {
        if !output.stdout.is_empty() {
            println!("Ollama is already running.");
            return None;
        }
    }
    println!("Starting Ollama server...");
    let ollama_process = Command::new("ollama")
        .arg("serve")
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .expect("Failed to start Ollama server");
    // Give Ollama a few seconds to start
    thread::sleep(Duration::from_secs(5));
    Some(ollama_process)
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

#[allow(dead_code)]
fn wait_for_backend_ready() -> bool {
    for i in 0..30 {
        if let Ok(resp) = reqwest::blocking::get("http://localhost:8000/api/status") {
            if resp.status().is_success() {
                if let Ok(text) = resp.text() {
                    if text.contains("ready") {
                        println!("✅ Backend is ready!");
                        return true;
                    }
                }
            }
        }
        println!("⏳ Waiting for backend to be ready... ({}/30)", i + 1);
        thread::sleep(Duration::from_secs(2));
    }
    false
}

fn main() {
    // Start Ollama and backend, store handles in Arc<Mutex<Option<Child>>>
    let ollama_handle = Arc::new(Mutex::new(start_ollama()));
    let backend_handle = Arc::new(Mutex::new(Some(start_backend())));

    let ollama_handle_clone = ollama_handle.clone();
    let backend_handle_clone = backend_handle.clone();

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![chat, set_glass_mode])
        .setup(|app| {
            let app_handle = app.handle();
            // Listen for window close event
            app_handle.listen_global("tauri://close-requested", move |_event| {
                // Kill backend
                if let Some(mut backend) = backend_handle_clone.lock().unwrap().take() {
                    let _ = backend.kill();
                }
                // Kill Ollama
                if let Some(mut ollama) = ollama_handle_clone.lock().unwrap().take() {
                    let _ = ollama.kill();
                }
            });
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|_app_handle, event| {
            if let RunEvent::WindowEvent { event: WindowEvent::CloseRequested { .. }, .. } = event {
                // This will trigger the close-requested event above
            }
        });
} 