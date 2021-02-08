<script>
    import {Router} from "@roxi/routify";
    import {routes} from "../.routify/routes";
</script>

<style global>
    body {
        padding: 0;
        margin: 0;
        font-family: FreeSans -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    }
</style>

<Router config="{{useHash: true}}" {routes}/>