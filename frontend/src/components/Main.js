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
import { Link } from 'react-router-dom';

export default function Album() {
  const [url, setUrl] = React.useState("");
  const [title, setTitle] = React.useState("");
  const [isUrlSubmitted, setIsUrlSubmitted] = React.useState(false);

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };
  const handleFindVideo = () => {
    api.get("/title", { params: { url: url } }).then((res) => {
      console.log(res.data);
    });
  };
  const handleGenerateVideo = () => {
    api.get("/generate", { params: { url: url } }).then((res) => {
      console.log(res.data);
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
          <Typography
            variant="h6"
            align="center"
            color="text.secondary"
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
                },
              }}
            />
            {isUrlSubmitted && (
              <TextField
                variant="outlined"
                fullWidth
                value={title}
                disabled
                InputProps={{
                  sx: {
                    borderRadius: "10px",
                  },
                }}
              />
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
