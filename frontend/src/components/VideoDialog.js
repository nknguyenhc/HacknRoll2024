import api from "../api";
import { Dialog, DialogContent, Typography } from "@mui/material";
import ReactPlayer from "react-player";
import { useState, useEffect } from "react";
import { enqueueSnackbar } from "notistack";

function VideoDialog({ open, handleClose, title, vidId }) {
  const [videoExists, setVideoExists] = useState(true);

  useEffect(() => {
    const checkVideoExists = () => {
      api
        .get(`content/${vidId}`)
        .then((response) => {
          if (response.status === 204) {
            enqueueSnackbar("Video is still generating", { variant: "info" });
          }
        })
        .catch((error) => {
          setVideoExists(false);
        });
    };

    if (vidId) {
      checkVideoExists();
      if (!videoExists) {
        // Remove vidId from localStorage
        let pastVideos = JSON.parse(localStorage.getItem("pastVideos")) || [];
        pastVideos = pastVideos.filter((video) => video.id !== vidId);
        localStorage.setItem("pastVideos", JSON.stringify(pastVideos));
        // Add to snackbar
        enqueueSnackbar("Video was failed to generate", { variant: "error" });
      }
    }
  }, [vidId, videoExists]);

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
        {videoExists && (
          <ReactPlayer
            url={`content/${vidId}`}
            controls={true}
            playing={true}
          />
        )}
      </DialogContent>
    </Dialog>
  );
}

export default VideoDialog;
