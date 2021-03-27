import {useCallback, useState} from "react";
import Log from "./log";
import {Tab, Tabs, ImagesGrid, ClickableImage} from './shared';


const ResultImage = ({url, createdAt}) => {
    createdAt = new Date(createdAt).toISOString().slice(0, 19).replace(/[-:T]/g, '_');

    return (
        <div className="container grid-lg">
            <ClickableImage src={url} alt={url} url={url} filename={`result_${createdAt}.jpg`} id="result"/>
        </div>
    )
}


const Snapshot = ({scan}) => {
    const [activeTab, setActiveTab] = useState('result');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    const images = {original: {}, undistorted: {}, projected: {}, result: scan.images.result};
    for (const name of ['original', 'undistorted', 'projected']) {
        for (const position of ['LU', 'LL', 'RU', 'RL']) {
            const {image, thumb} = scan.images[name][position];
            images[name][position] = {src: thumb, alt: image, url: image};
        }
    }

    return (
        <div>
            <Tabs>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" isActive={activeTab === "undistorted"}/>
                <Tab onClick={selectTab} name="projected" text="Projected" isActive={activeTab === "projected"}/>
                <Tab onClick={selectTab} name="result" text="Result" isActive={activeTab === "result"}/>
                <Tab onClick={selectTab} name="log" text="Log" isActive={activeTab === "log"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={images.original} isClickable/>}
            {activeTab === "undistorted" && <ImagesGrid images={images.undistorted} isClickable/>}
            {activeTab === "projected" && <ImagesGrid images={images.projected} isClickable/>}
            {activeTab === "result" && <ResultImage url={images.result.image} createdAt={scan.createdAt}/>}
            {activeTab === "log" && <Log text={scan.log}/>}
        </div>
    )
}


export default Snapshot;