import {useState, useEffect, useCallback} from 'react'


const useFetch = (url) => {
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    const [options, setOptions] = useState({});
    const [query, setQuery] = useState('');

    const doFetch = useCallback((options = {}, query = '') => {
        if (!options.headers)
            options.headers = {};

        if (!options.headers['Content-Type'])
            options.headers['Content-Type'] = 'application/json';

        if (query.length > 0)
            query = '?' + query

        setOptions(options);
        setQuery(query);
        setIsLoading(true);
    }, []);

    useEffect(() => {
        let skipGetResponseAfterDestroy = false;

        if (!isLoading)
            return;

        async function _fetch() {
            try {
                const response = await fetch(url + query, options);
                console.log(response);
                const json = await response.json();

                if (!skipGetResponseAfterDestroy) {
                    if (!response.ok)
                        throw new Error(json.message);

                    setResponse(json);
                    setIsLoading(false);
                }
            } catch (error) {
                if (!skipGetResponseAfterDestroy) {
                    setError(error.message);
                    setIsLoading(false);
                }
            }
        }

        _fetch();

        return () => {
            skipGetResponseAfterDestroy = true;
        }
    }, [isLoading, url, options, query]);

    return [{isLoading, response, error}, doFetch];
};


export default useFetch;