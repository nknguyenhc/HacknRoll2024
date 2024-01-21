import { Dialog, DialogContent, Typography } from "@mui/material";
import ReactPlayer from "react-player";

function VideoDialog({ open, handleClose, title, vidId }) {
  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogContent
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <Typography
          variant="h6"
          align="center"
          color="primary"
          sx={{
            borderRadius: "10px",
            textAlign: "center",
            fontWeight: "800",
          }}
        >
          Video Title: {title}
        </Typography>
        <ReactPlayer
            url={`content/${vidId}`}
            controls={true}
            playing={true}
          />
      </DialogContent>
    </Dialog>
  );
}

export default VideoDialog;
