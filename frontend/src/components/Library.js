import VideoDialog from "./VideoDialog";
import { Container, Grid, Card, CardContent, Typography, Box, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { useEffect, useState } from "react";

export default function Library() {
  const [pastVideos, setPastVideos] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(() => {
    const storedVideos = JSON.parse(localStorage.getItem("pastVideos")) || [];
    setPastVideos(storedVideos);
    console.log(storedVideos);
  }, []);

  const handleDialogClose = () => {
    setDialogOpen(false);
  };

  const handleCardClick = (video) => {
    setSelectedVideo(video);
    setDialogOpen(true);
  };

  const handleDeleteClick = (event, videoToDelete) => {
    event.stopPropagation();
    const updatedVideos = pastVideos.filter(video => video.id !== videoToDelete.id);
    setPastVideos(updatedVideos);
    localStorage.setItem('pastVideos', JSON.stringify(updatedVideos));
  };

  return (
    <Box
      sx={{
        bgcolor: "background.paper",
        width: "100vw",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Container maxWidth="md">
        <Grid container spacing={4}>
          {pastVideos.map((video) => (
            <Grid item key={video.id} xs={12} sm={6} md={4}>
              <Card onClick={() => handleCardClick(video)}>
                <CardContent>
                  <Typography gutterBottom variant="h6" component="h2" color={"primary"} fontWeight="800">
                    {video.title}
                  </Typography>
                  <Typography>
                    Generated at: {new Date(video.timestamp).toLocaleString()}
                  </Typography>
                  <IconButton onClick={(event) => handleDeleteClick(event, video)}>
                    <DeleteIcon />
                  </IconButton>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
        {selectedVideo && (
          <VideoDialog
            open={dialogOpen}
            handleClose={handleDialogClose}
            title={selectedVideo.title}
            vidId={selectedVideo.id}
          />
        )}
      </Container>
    </Box>
  );
}
