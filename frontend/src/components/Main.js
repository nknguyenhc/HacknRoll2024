import * as React from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import YouTubeIcon from "@mui/icons-material/YouTube";
import InputAdornment from "@mui/material/InputAdornment";
import api from "../api";
import { useState } from "react";
import { useSnackbar } from 'notistack';

export default function Album() {
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [isUrlSubmitted, setIsUrlSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [generatedUrl, setGeneratedUrl] = useState('');
  const { enqueueSnackbar } = useSnackbar();

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };
  const handleFindVideo = () => {
    api.get("/title", { params: { url: url } }).then((res) => {
      console.log(res.data);
      setTitle(res.data.title);
      setIsUrlSubmitted(true);
    }).catch((err) => {
      console.log(err);
      enqueueSnackbar('Video not found', { variant: 'error' });
    });
  };
  const handleGenerateVideo = () => {
    setLoading(true);
    setLoading(false);
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
          <Typography
            variant="h6"
            align="center"
            color="secondary"
            paragraph
          >
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
        </Container>
      </Box>
    </main>
  );
}
