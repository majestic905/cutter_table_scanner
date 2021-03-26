import {useCallback, useState} from "react";
import {Tab, Tabs, ImagesGrid, ClickableImage} from './shared';


const ResultImage = (props) => {
    return (
        <div className="container grid-lg">
            <ClickableImage {...props}/>
        </div>
    )
}


const Snapshot = ({scan}) => {
    const [activeTab, setActiveTab] = useState('result');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    const images = {};
    for (const name of ['original', 'undistorted', 'projected']) {
        images[name] = {};
        for (const position of ['LU', 'LL', 'RU', 'RL']) {
            const src = scan.images[name][position].thumb;
            images[name][position] = {src, alt: src};
        }
    }
    images.result = {
        src: scan.images.result.thumb,
        alt: scan.images.result.thumb,
        url: scan.images.result.image,
        filename: `${scan.scanId}_result.jpg`
    }

    return (
        <div>
            <Tabs>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" isActive={activeTab === "undistorted"}/>
                <Tab onClick={selectTab} name="projected" text="Projected" isActive={activeTab === "projected"}/>
                <Tab onClick={selectTab} name="result" text="Result" isActive={activeTab === "result"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={images.original}/>}
            {activeTab === "undistorted" && <ImagesGrid images={images.undistorted}/>}
            {activeTab === "projected" && <ImagesGrid images={images.projected}/>}
            {activeTab === "result" && <ResultImage {...images.result}/>}
        </div>
    )
}


export default Snapshot;