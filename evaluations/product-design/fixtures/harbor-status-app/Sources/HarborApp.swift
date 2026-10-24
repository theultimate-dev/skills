import SwiftUI

@main
struct HarborApp: App {
    var body: some Scene {
        MenuBarExtra("Harbor", systemImage: "externaldrive") {
            StatusView()
        }
        .menuBarExtraStyle(.window)

        Settings {
            SettingsView()
        }
    }
}

struct StatusView: View {
    var body: some View {
        Text("Backup status")
            .padding()
    }
}

struct SettingsView: View {
    var body: some View {
        Text("Settings")
            .padding()
    }
}
