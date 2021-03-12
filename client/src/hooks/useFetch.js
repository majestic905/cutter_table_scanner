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
        setError(undefined);
    }, []);


    useEffect(() => {
        if (!isLoading)
            return;

        let isUnmounted = false;

        async function sendRequest() {
            try {
                const json = await ky(url, options).json();

                if (isUnmounted)
                    return;

                setResponse(json);
                setIsLoading(false);
            } catch (error) {
                if (isUnmounted)
                    return;

                if (error.name === 'HTTPError')
                    setError((await error.response.json()).message);
                else
                    setError(error.message);
                setIsLoading(false);
            }
        }

        sendRequest();

        return () => {
            isUnmounted = true;
        };
    }, [isLoading, url, options]);

    return [{isLoading, response, error}, doFetch];
};


export default useFetch;