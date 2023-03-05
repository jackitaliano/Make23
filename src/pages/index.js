import { useEffect, useRef, useState } from "react";
import { getDatabase, off, onValue, ref } from "firebase/database";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Jumbotron } from 'react-bootstrap';
import { remark } from 'remark'
import html from 'remark-html'

export default function Home() {
  const [transcribe, setTranscribe] = useState([]);
  const [notes, setNotes] = useState("")
  const [subTopics, setSubTopics] = useState([])
  const [images, setImages] = useState([])

  const database = getDatabase()

  const processedContent = async (markdown) => {
    const processed = await remark().use(html).process(markdown);
    const content = processed.toString
    return content;
  };


  useEffect(() => {
    let newSentenceRef = ref(database, "/NewSentence")
    onValue(newSentenceRef, (snapshot) => {
      if(snapshot.exists()){
        const newItem = snapshot.val();
        console.log(newItem);
        if(newItem.length != 0)
        setTranscribe((prevItems) => [...prevItems, newItem]);
      }
    })
    return () => {
      off(newSentenceRef);
    }

  }, []);

  useEffect(() => {
    // Attach event listener for "item2" data point
    let summarizedDataRef = ref(database, "/SummarizedData")
    onValue(summarizedDataRef, (snapshot) => {
      if(snapshot.exists()){
        const item = decodeURIComponent(snapshot.val());
        console.log(item);
        if(item.length != 0)
          setNotes(item);
      }
    })
    return () => {
      off(summarizedDataRef)
    }
  }, [])

  useEffect(() => {
    let imagesRef = ref(database, "/RelatedImages")
    onValue(imagesRef, (snapshot) => {
      if(snapshot.exists()){
        const newItem = snapshot.val();
        console.log(newItem);
        if(newItem.length != 0){
          const linkedImg = "<img src=" + newItem + ">"
          setImages((prevItems) => [...prevItems, linkedImg]);
        }
      }
    })
    return () => {
      off(imagesRef);
    }

  }, []);

  useEffect(() => {
    let subTopicsRef = ref(database, "/RelatedLinks")
    onValue(subTopicsRef, (snapshot) => {
      if(snapshot.exists()){
        const newItem = snapshot.val();
        console.log(newItem);
        if(newItem.length != 0){
          const splitComponents = newItem.split("~");
          const linkedRef = "<a href =" + splitComponents[0] + ">" + splitComponents[1] + "</li>"
          setSubTopics((prevItems) => [...prevItems, linkedRef]);
        }
      }
    })
    return () => {
      off(subTopicsRef);
    }

  }, []);

  return (
    <div className="text-center">
      <h1 className = "display-3">Note to Audio Dashboard</h1>
      <div className = "row">
        <div className = "col-md-6">
          <h6  className = "display-5 d-flex justify-content-start">Transcript</h6>
          <div className="d-flex justify-content-start">
          <ul>
          {transcribe.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
          </ul>
          </div>
        </div>
        <div className = "col-md-6">
          <h6 className = "display-5 d-flex justify-content-start">Notes</h6>
          <div dangerouslySetInnerHTML={{ __html: notes }}>
          </div>
          <div>
            <h2 className = "display-5 d-flex justify-content-start">Related Topics</h2>
            <ul>
            {subTopics.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
            </ul>
          </div>
          <div>
            <h2 className = "display-5 d-flex justify-content-start">Related Images</h2>
            <ul>
            {images.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
