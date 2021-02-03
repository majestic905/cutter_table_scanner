import {useCallback} from "react";
import logo from "../logo.svg";


const ScanButton = ({onCreate}) => {
    const doCreate = useCallback(() => {
        fetch('/api/scans', {method: 'POST'})
            .then(onCreate)
            .catch(error => console.error(error));
    }, [onCreate]);

    return (
        <span className='header-button' onClick={doCreate}>
            Сканировать
        </span>
    )
}


const Images = ({loadScans}) => {
    return (
        <div className="no-scrollbar" id="column-images">
            <h5 className="d-inline">Изображения</h5>
            <ScanButton onCreate={loadScans}/>

            <div className="columns">
                <div className="column col-5">
                    <div className="columns">
                        <div className="column col-6">
                            <img className="img-responsive" src={logo} alt="Image #1"/>
                        </div>
                        <div className="column col-6">
                            <img className="img-responsive" src={logo} alt="Image #2"/>
                        </div>
                        <div className="column col-6">
                            <img className="img-responsive" src={logo} alt="Image #3"/>
                        </div>
                        <div className="column col-6">
                            <img className="img-responsive" src={logo} alt="Image #4"/>
                        </div>
                    </div>
                </div>

                <div className="column col-7">
                    <img className="img-responsive" src='/logo512.png' alt="Image #4"/>
                </div>
            </div>
        </div>
    )
}

export default Images;