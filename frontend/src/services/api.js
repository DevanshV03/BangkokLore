const API_BASE_URL = 'http://localhost:5000';


export const storyAPI = {
    getAllStories: async () =>{
        try{
            const response = await fetch(`${API_BASE_URL}/api/getstories`);
            const data = await response.json();
            if(data.success){
                return data.stories;
            }
            else{
                throw new Error(data.error || "No Stories found");
            }
        }
        catch(error){
            console.error("error fetching stories",error);
            throw error;
        }
    },
    
    submitStory: async (storyData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/submit-lore`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(storyData)
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        return data;
      } else {
        throw new Error(data.error || 'Failed to submit story');
      }
    } catch (error) {
      console.error('Error submitting story:', error);
      throw error;
    }
  }
};