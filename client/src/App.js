import {useState, useEffect} from "react";
import logo from './logo.svg';
import './App.css';


function App() {
    const [currentTime, setCurrentTime] = useState(0);

    useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
    }, []);

    return (
        <main className="container">
            <div className="columns">
                <div className="column">
                  File tree here
                </div>

                <div className="divider-vert"/>

                <div className="column" id="column-images">
                    <div className="columns" id="container-images">
                        <div className="column col-6">
                            <figure className="figure">
                                <img className="img-responsive" src={logo} alt="Image #1"/>
                                <figcaption className="figure-caption text-center">Image #1</figcaption>
                            </figure>
                        </div>
                        <div className="column col-6">
                            <figure className="figure">
                                <img className="img-responsive" src={logo} alt="Image #2"/>
                                <figcaption className="figure-caption text-center">Image #2</figcaption>
                            </figure>
                        </div>
                        <div className="column col-6">
                            <figure className="figure">
                                <img className="img-responsive" src={logo} alt="Image #3"/>
                                <figcaption className="figure-caption text-center">Image #3</figcaption>
                            </figure>
                        </div>
                        <div className="column col-6">
                            <figure className="figure">
                                <img className="img-responsive" src={logo} alt="Image #4"/>
                                <figcaption className="figure-caption text-center">Image #4</figcaption>
                            </figure>
                        </div>
                    </div>

                    <hr/>

                    {/*<figure className="figure">*/}
                    {/*    <img className="img-responsive" src='/logo512.png' alt="Image #4"/>*/}
                    {/*</figure>*/}
                </div>

                <div className="divider-vert"/>

                <div className="column" id="column-textarea">
                  <textarea className="form-input" readOnly/>
                </div>
            </div>
        </main>
    );
}

export default App;
