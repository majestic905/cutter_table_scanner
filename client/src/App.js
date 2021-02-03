import {useState, useEffect, useCallback} from "react";

import ScansList from "./components/scans_list";
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

    // ------------

    const [selectedScan, setSelectedScan] = useState(null);


    return (
        <main className="container">
            <div className="columns">
                <ScansList size={3} selectedScan={selectedScan} selectScan={setSelectedScan} />

                <Images size={5} />

                <Log size={4} logItems={logItems}/>
            </div>
        </main>
    );
}

export default App;
