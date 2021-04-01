import {useCallback, useState} from "react";
import Log from "./log";
import {Tabs, Tab} from "./shared/tabs";
import {ImagesGrid, DownloadableImage} from "./shared/images";


function transformUrls({thumb, image}, createdAt) {
    return {src: `${thumb}?${createdAt}`, alt: image, url: image};
}


const ResultImage = ({url, createdAt}) => {
    const src = `${url}?${createdAt}`;

    createdAt = new Date(createdAt).toISOString().slice(0, 19).replace(/[-:T]/g, '_');
    const download = `result_${createdAt}.jpg`

    return (
        <div className="container grid-lg">
            <DownloadableImage src={src} alt={url} url={url} download={download} id="result"/>
        </div>
    )
}


const Snapshot = ({scan}) => {
    const [activeTab, setActiveTab] = useState('result');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    const images = {original: {}, projected: {}, result: scan.images.result};
    for (const name of ['original', 'projected'])
        for (const position of ['LU', 'LL', 'RU', 'RL'])
            images[name][position] = transformUrls(scan.images[name][position], scan.createdAt);

    return (
        <div>
            <Tabs>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="projected" text="Projected" isActive={activeTab === "projected"}/>
                <Tab onClick={selectTab} name="result" text="Result" isActive={activeTab === "result"}/>
                <Tab onClick={selectTab} name="log" text="Log" isActive={activeTab === "log"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={images.original} isClickable/>}
            {activeTab === "projected" && <ImagesGrid images={images.projected} isClickable/>}
            {activeTab === "result" && <ResultImage url={images.result.image} createdAt={scan.createdAt}/>}
            {activeTab === "log" && <Log text={scan.log}/>}
        </div>
    )
}


export default Snapshot;