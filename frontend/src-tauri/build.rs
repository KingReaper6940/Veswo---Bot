use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    // Only run on macOS bundle builds
    if cfg!(target_os = "macos") {
        let out_dir = env::var("OUT_DIR").unwrap();
        // OUT_DIR is something like .../target/release/build/veswo1-bot-*/out
        // The .app bundle is a few directories up
        let mut bundle_path = PathBuf::from(&out_dir);
        for _ in 0..6 { bundle_path.pop(); }
        bundle_path.push("bundle/macos/veswo1-bot.app/Contents/Resources");

        // Copy backend
        let backend_src = PathBuf::from("../../backend");
        let backend_dst = bundle_path.join("backend");
        if backend_src.exists() {
            let _ = fs::remove_dir_all(&backend_dst);
            let _ = fs_extra::dir::copy(
                &backend_src,
                &bundle_path,
                &fs_extra::dir::CopyOptions::new().content_only(true).overwrite(true),
            );
        }

        // Copy launcher.sh
        let launcher_src = PathBuf::from("../../launcher.sh");
        let launcher_dst = bundle_path.join("launcher.sh");
        if launcher_src.exists() {
            let _ = fs::copy(&launcher_src, &launcher_dst);
        }

        // Copy requirements.txt
        let reqs_src = PathBuf::from("../../requirements.txt");
        let reqs_dst = bundle_path.join("requirements.txt");
        if reqs_src.exists() {
            let _ = fs::copy(&reqs_src, &reqs_dst);
        }
    }
} 