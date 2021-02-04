import {useCallback} from "react";


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


const Image = ({selectedScan}) => {
    const imgSrc = `/api/scans/${selectedScan.name}`;
    // const imgUrl = `/api/scans/${selectedScan.name}?as_attachment=true`;
    const imgUrl = `${imgSrc}?as_attachment=true`;

    return (
        <div>
            <p className="text-italic mb-2">Кликните, чтобы скачать</p>
            <a href={imgUrl}>
                <img className="img-responsive"
                     src={imgSrc}
                     alt={selectedScan.name}
                />
            </a>
        </div>
    )
}


const ScanResult = ({loadScans, selectedScan}) => {
    return (
        <div id="scan-result">
            <header className="mb-2">
                <h5 className="d-inline">Изображение</h5>
                <ScanButton onCreate={loadScans}/>
            </header>

            {selectedScan
                ? <Image selectedScan={selectedScan}/>
                : <p className="text-italic">Выберите скан из списка</p>
            }
        </div>
    )
}

export default ScanResult;