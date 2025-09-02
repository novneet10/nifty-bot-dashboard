import diagnostics
import auto_correct

def run_launch_check():
    print("🚀 Starting pre-market launch check...\n")

    issues = []

    # Run diagnostics and collect results
    config_status = diagnostics.check_config()
    print(config_status)
    if "❌" in config_status:
        issues.append("config")

    try:
        with open("config.yaml", "r") as f:
            import yaml
            config = yaml.safe_load(f)
        slack_status = diagnostics.check_slack(config["slack"]["webhook_url"])
        print(slack_status)
        if "❌" in slack_status:
            issues.append("slack")
    except:
        print("⚠️ Skipping Slack check due to config error")
        issues.append("slack")

    sqlite_status = diagnostics.check_sqlite()
    print(sqlite_status)
    if "❌" in sqlite_status:
        issues.append("sqlite")

    token_status = diagnostics.check_token_mapping()
    print(token_status)
    if "❌" in token_status:
        issues.append("token")

    # Auto-correct if needed
    if issues:
        print("\n🛠️ Issues detected:", issues)
        print("🔧 Running auto-correct...\n")
        if "config" in issues:
            auto_correct.fix_config()
        if "sqlite" in issues:
            auto_correct.fix_sqlite()
        if "token" in issues:
            auto_correct.fix_token_mapping()
        print("\n✅ Auto-correction complete. Re-run diagnostics to confirm.")
    else:
        print("\n✅ All systems go. You're ready to launch.")

if __name__ == "__main__":
    run_launch_check()
