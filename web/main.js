$(document).ready(function () {
    $("#encrypt").click(function () {
        jsencrypt($("#data1")[0].value, $("#key1")[0].value, $("#encrypted"));
    });
    $("#decrypt").click(function () {
        jsdecrypt($("#data2")[0].value, $("#key2")[0].value, $("#decrypted"));
    });

    async function jsencrypt(message, key, output) {
        let value = await eel.encrypt(message, key)();
        output.text(value);
        return value;
    }

    async function jsdecrypt(message, key, output) {
        let value = await eel.decrypt(message, key)();
        output.text(value);
        return value;
    }
});