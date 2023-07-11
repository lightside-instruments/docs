channels

pkg load signal
figure(1)
plot(ch1,'r')
hold on
plot(ch2,'b')
disp("filter")

signal = ((ch1-ch2)-mean(ch1-ch2))(1:20000)

figure(2)
plot(signal)

fs=200000000
fc=20000000

[b,a] = butter(20,fc/(fs/2));
signal_f=filter(b,a,signal)
figure(3)
plot(signal_f)


signal_b = signal;
signal_b(signal_b > 0.8) = 1;
signal_b(signal_b <= 0.8) = 0;

figure(4)
plot(signal_b)

for c = 1:(floor(length(signal_b)+19)/20)
    a(c)=sum(signal_b(20*(c-1)+1:20*c).*2.^[19:-1:0])
end

fileID = fopen('signal.bin','w');
fwrite(fileID,a,'uint32','ieee-le');
fclose(fileID);

signal_b = signal_f;
signal_b(signal_b > 0.8) = 1;
signal_b(signal_b <= 0.8) = 0;

figure(4)
plot(signal_b)

for c = 1:(floor(length(signal_b)+19)/20)
    a(c)=sum(signal_b(20*(c-1)+1:20*c).*2.^[19:-1:0])
end

fileID = fopen('signal_f.bin','w');
fwrite(fileID,a,'uint32','ieee-le');
fclose(fileID);
