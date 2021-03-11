import {useCallback, useState} from "react";
import {Tab, Tabs, ImagesGrid} from './shared';


const ResultImage = ({src, scanId}) => {
    const doDownloadFile = useCallback(() => {
        fetch(src)
          .then(resp => resp.blob())
          .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `${scanId}.jpg`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
          })
          .catch(error => {
              console.error(error);
              alert(error.message);
          });
    }, [src, scanId]);

    return (
        <img className="img-responsive c-hand" src={src} alt={src} onClick={doDownloadFile}/>
    )
}


const Snapshot = ({scan}) => {
    const [activeTab, setActiveTab] = useState('original');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    return (
        <div>
            <Tabs activeTab={activeTab} selectTab={selectTab}>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" isActive={activeTab === "undistorted"}/>
                <Tab onClick={selectTab} name="projected" text="Projected" isActive={activeTab === "projected"}/>
                <Tab onClick={selectTab} name="result" text="Result" isActive={activeTab === "result"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={scan.images.original}/>}
            {activeTab === "undistorted" && <ImagesGrid images={scan.images.undistorted}/>}
            {activeTab === "projected" && <ImagesGrid images={scan.images.projected}/>}
            {activeTab === "result" && <ResultImage src={scan.images.result} scanId={scan.scanId}/>}
        </div>
    )
}


export default Snapshot;