import type {Headline, Info, Journal} from "./internal";
import {apiURL} from "./index";
import {HeadlineFromJSON, InfoFromJSON, JournalFromJSON} from "./internal";

export class Updates<T> {
    private ws?: WebSocket = null;
    private scheduler?: number = null;

    constructor(private readonly url: string,
                private readonly callback: (value) => any,
                private readonly factory: (json: any) => T,
                private readonly interval: number = 3000) {
        if (url) {
            this.connect();
        }
    }

    close() {
        if (this.ws) {
            this.ws.close()
            this.ws = null;
        }
        if (this.scheduler) {
            clearTimeout(this.scheduler);
        }
    }

    private connect() {
        this.scheduler = null;
        if (!this.url) {
            return
        }
        this.ws = new WebSocket(this.url);

        this.ws.onclose = () => {
            this.ws = null;
            this.scheduler = setTimeout(this.connect, this.interval);
        }
        this.ws.onmessage = (event) => {
            const pd = this.factory(JSON.parse(event.data));
            this.callback(pd);
        }
    }
}

function wsURL(resource: string): string {
    let url = new URL(apiURL + resource, document.baseURI);
    url.protocol = url.protocol === "https" ? "wss" : "ws";
    return url.href.toString()
}

export function journalsHeadlines(callback: (value: Headline) => any): Updates<Headline> {
    return new Updates<Headline>(wsURL("/internal/journals/updates"), callback, HeadlineFromJSON)
}

export function journalUpdates(id: number, callback: (value: Journal) => any): Updates<Journal> {
    return new Updates<Journal>(wsURL(`/internal/journal/${id}/updates`), callback, JournalFromJSON)
}


export function servicesUpdates(callback: (value: Info) => any): Updates<Info> {
    return new Updates<Info>(wsURL(`/internal/services/updates`), callback, InfoFromJSON)
}