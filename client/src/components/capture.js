import {useCallback, useState} from "react";
import Log from "./log";
import {Tabs, Tab} from "./shared/tabs";
import {ImagesGrid} from "./shared/images";


const Capture = ({scan}) => {
    const [activeTab, setActiveTab] = useState('original');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    const images = {original: {}};
    for (const name in images) {
        for (const position of ['LU', 'LL', 'RU', 'RL']) {
            const {image, thumb} = scan.images[name][position];
            images[name][position] = {src: `${thumb}?${scan.createdAt}`, alt: image, url: image};
        }
    }

    return (
        <div>
            <Tabs>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="log" text="Log" isActive={activeTab === "log"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={images.original} isClickable/>}
            {activeTab === "log" && <Log text={scan.log}/>}
        </div>
    )
}


export default Capture;