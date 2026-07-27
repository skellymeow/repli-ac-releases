import { defaultEveAuth, eveChannel } from "eve/channels/eve";
import { localDev } from "eve/channels/auth";

// Stitch is a loopback desktop application. The sidecar binds to 127.0.0.1,
// and Eve additionally admits only the local development principal.
export default eveChannel({
  auth: [localDev()],
  cors: false,
  onMessage(ctx, message) {
    const text = typeof message === "string" ? message : "";
    return {
      auth: defaultEveAuth(ctx),
      context: [
        "This message originated from the local Stitch native desktop client.",
        text.includes("[AUTO MODE]")
          ? "Auto mode is enabled. Complete the inspect, plan, build, verify loop autonomously."
          : "Interactive mode is enabled. Keep the user informed before consequential edits.",
      ],
    };
  },
});
