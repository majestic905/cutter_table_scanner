import {useState, useEffect, useCallback} from "react";

import Files from "./components/files";
import Images from "./components/images";
import Log from "./components/log";
import Divider from "./components/divider";

import './App.scss';


function generateMessage(text) {

}


function App() {
    const [logItems, setLogItems] = useState([]);

    const addLogItem = useCallback((message) => {
        const item = {timestamp: new Date(), message};
        setLogItems(items => [item, ...items]);
    }, [setLogItems]);

    useEffect(() => {
        addLogItem("App initialized");
    }, []);


    return (
        <main className="container">
            <div className="columns">
                <Files />

                <Divider />

                <Images />

                <Divider />

                <Log logItems={logItems}/>
            </div>
        </main>
    );
}

export default App;
