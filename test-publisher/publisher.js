var amqp = require('amqplib/callback_api');
var randomstring = require('randomstring');
var args = require('args');
var randomUnicode = require('random-unicodes');

function bail(err) {
    console.error(err);
    process.exit(1);
}

function checkArgs(flags) {
    if (flags.amqpUrl === undefined || flags.queue === undefined) {
        return false;
    } else {
        return true;
    }
}

args.option('amqp-url', 'amqp url')
    .option('queue', 'queue name')
    .option('interval', 'interval', 2000);

const flags = args.parse(process.argv);

if (!checkArgs(flags)) {
    console.log('   check arguments!')
} else {
    const amqpUrl = flags.amqpUrl;
    const queue = flags.queue;
    const interval = flags.interval;


    amqp.connect(amqpUrl, function (err, conn) {
        if (err !== null) bail(err);

        conn.createChannel(on_open);

        function on_open(err, ch) {
            var count = 0;
            setInterval(function () {
                if (err !== null) bail(err);

                ch.assertQueue(queue);

                var messageObj = {};
                messageObj.userId = randomstring.generate({length: 10, charset: 'alphanumeric'});
                messageObj.count = count;
                messageObj.unicodes = [];

                // 유니코드 지정하려면 수정 (랜덤한 갯수의 랜덤한 한글 유니코드를 unicodes 어레이에 푸시)
                const randomCount = randomstring.generate({length: 1, charset: 'numeric'}) * 1 + 1;

                for (var i = 0; i < randomCount; i++) {
                    // 한글 유니코드 ac00 ~ d7a3
                    const korRandomUnicodeBefore = randomUnicode({min: '\\uAC00', max: '\\uD7A3'});
                    const korRandomUnicode = korRandomUnicodeBefore.substring(2,6).toLowerCase();
                    messageObj.unicodes.push(korRandomUnicode)
                }

                var message = JSON.stringify(messageObj);

                ch.sendToQueue(queue, new Buffer(message));

                count++;
                console.log('-----------------------------');
                console.log(messageObj);
                console.log('-----------------------------');
            }, interval)

        }
    });

}

