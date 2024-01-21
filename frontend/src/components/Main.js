import { useState, useCallback } from "react";
import VideoDialog from "./VideoDialog";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import LinearProgress from "@mui/material/LinearProgress";
import YouTubeIcon from "@mui/icons-material/YouTube";
import InputAdornment from "@mui/material/InputAdornment";
import api from "../api";
import { useSnackbar } from "notistack";
import { usePageContext } from "../context";

export default function Main() {
  const { url, setUrl, isUrlSubmitted, setIsUrlSubmitted } = usePageContext();
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
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
        enqueueSnackbar(err.response.data.detail, { variant: "error" });
      });
  };
  const handleGenerateVideo = useCallback(() => {
    if (loading) {
      return;
    }
    setLoading(true);
    api
      .get("/video", { params: { url: url } })
      .then((res) => {
        const videoData = {
          id: res.data.id,
          title: res.data.title,
          timestamp: new Date().toISOString(),
        };
        setVidId(videoData.id);
        enqueueSnackbar("Video started generating", { variant: "success" });
        enqueueSnackbar("Wait or watch it later in the library", {
          variant: "info",
        });
        enqueueSnackbar("If video fails to load after too long, try generating again", {
          variant: "warning",
        });
        setOpen(true);
        let pastVideos = JSON.parse(localStorage.getItem("pastVideos")) || [];
        pastVideos.push(videoData);
        localStorage.setItem("pastVideos", JSON.stringify(pastVideos));
      })
      .catch((err) => {
        enqueueSnackbar(err.response.data.detail, { variant: "error" });
      })
      .finally(() => {
        setLoading(false);
      });
  }, [loading, enqueueSnackbar, url]);

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
          {loading && <LinearProgress color="secondary" />}
        </Container>
      </Box>

      <VideoDialog
        open={open}
        handleClose={handleClose}
        title={title}
        vidId={vidId}
      />
    </main>
  );
}
