import {useState, useEffect, useCallback} from 'react'
import ky from 'ky';


const useFetch = (url) => {
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState(undefined);
    const [error, setError] = useState(undefined);
    const [options, setOptions] = useState({});


    const doFetch = useCallback((options = {}) => {
        setOptions(options);
        setIsLoading(true);
    }, []);


    useEffect(() => {
        if (!isLoading)
            return;

        const abortController = new AbortController();
        const signal = abortController.signal;

        void async function sendRequest() {
            try {
                const json = await ky(url, {...options, signal}).json();
                setResponse(json);
                setIsLoading(false);
            } catch (error) {
                if (error.name === 'HTTPError') {
                    const json = await error.response.json();
                    setError(json.message);
                    setIsLoading(false);
                } else if (error.name !== 'AbortError') {
                    setError(error.message);
                    setIsLoading(false);
                }
            }
        }();

        return () => {
            abortController.abort();
        };
    }, [isLoading, url, options]);

    return [{isLoading, response, error}, doFetch];
};


export default useFetch;