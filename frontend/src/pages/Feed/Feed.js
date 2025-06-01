import React from "react";
import Header from "../../components/Layout/Header/Header";
import StoryGrid from "../../components/Stories/StoryGrid/StoryGrid";
import './Feed.css'

const Feed = () =>{
    return(
        <div className="feed">
        <Header isLandingPage={false}/>
        <StoryGrid/>
        </div>
    );
};

export default Feed;