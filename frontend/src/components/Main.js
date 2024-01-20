import * as React from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import LinearProgress from "@mui/material/LinearProgress";
import YouTubeIcon from "@mui/icons-material/YouTube";
import InputAdornment from "@mui/material/InputAdornment";
import api from "../api";
import { useState } from "react";
import ReactPlayer from "react-player";
import { useSnackbar } from "notistack";

export default function Album() {
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [isUrlSubmitted, setIsUrlSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = React.useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const [vidId, setVidId] = useState("");

  const handleClose = () => {
    setOpen(false);
  };
  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };
  const handleFindVideo = () => {
    api
      .get("/title", { params: { url: url } })
      .then((res) => {
        setTitle(res.data.title);
        setIsUrlSubmitted(true);
      })
      .catch((err) => {
        console.log(err);
        enqueueSnackbar("Video not found", { variant: "error" });
      });
  };
  const handleGenerateVideo = () => {
    setLoading(true);
    api
      .get("/video", { params: { url: url } })
      .then((res) => {
        setVidId(res.data.id);
        enqueueSnackbar("Video generated successfully", { variant: "success" });
        setOpen(true);
        setLoading(true);
      })
      .catch((err) => {
        console.log(err);
        enqueueSnackbar("Video generation failed", { variant: "error" });
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <main>
      <Box
        sx={{
          bgcolor: "background.paper",
          width: "100vw",
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Container maxWidth="sm">
          <Typography
            component="h1"
            variant="h4"
            align="center"
            color="primary"
            fontWeight="800"
            gutterBottom
          >
            Generate Your Own Music Video
          </Typography>
          <Typography variant="h6" align="center" color="secondary" paragraph>
            Parodies is an AI-Powered platform that generates a music video for
            any youtube video of your choice, at your command.
          </Typography>
          <Stack
            sx={{ pt: 4 }}
            direction="column"
            spacing={2}
            justifyContent="center"
          >
            <TextField
              variant="outlined"
              fullWidth
              value={url}
              onChange={handleUrlChange}
              disabled={isUrlSubmitted}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <YouTubeIcon />
                  </InputAdornment>
                ),
                sx: {
                  borderRadius: "10px",
                  // backgroundColor: "white",
                  // color: "black",
                  // "& input": {
                  //   textAlign: "center",
                  // },
                },
              }}
            />
            {isUrlSubmitted && (
              <Typography
                variant="body1"
                align="center"
                color="primary"
                sx={{
                  borderRadius: "10px",
                  backgroundColor: "white",
                  textAlign: "center",
                  padding: "10px",
                  fontWeight: "800",
                }}
              >
                Video Title: {title}
              </Typography>
            )}
            {isUrlSubmitted ? (
              <Button variant="contained" onClick={handleGenerateVideo}>
                Generate Video
              </Button>
            ) : (
              <Button variant="contained" onClick={handleFindVideo}>
                Find Video
              </Button>
            )}
          </Stack>
          {/* Add Linear Progress Bar here */}
          {loading && <LinearProgress color="secondary" />}
        </Container>
      </Box>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogContent
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <ReactPlayer
            url={`${api.defaults.baseURL}/content/${vidId}`}
            controls={true}
            playing={true}
          />
        </DialogContent>
      </Dialog>
    </main>
  );
}
